import base64
from typing import Optional
from pydantic import BaseModel, Field
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.schemas.email_models import DraftResult, _get_google_services

from agents import function_tool
from app.db.approvals import (
    async_session,
    get_active_pending_draft,
    upsert_email_approval,
)



@function_tool
async def draft_email(
    to_email: str, subject: str, body: str, session_id: str, telegram_chat_id: int
) -> DraftResult:
    """Creates a Gmail draft or UPDATES an existing pending draft for this session if revising.
    DOES NOT send the email.
    """
    gmail, _ = _get_google_services()
  
    raw_message = f"To: {to_email}\r\nSubject: {subject}\r\n\r\n{body}"
    encoded = base64.urlsafe_b64encode(raw_message.encode("utf-8")).decode("utf-8")
    draft_payload = {"message": {"raw": encoded}}

    async with async_session() as db:
        existing_approval = await get_active_pending_draft(session_id, db)

    if existing_approval:
        gmail_draft_id = existing_approval.payload["gmail_draft_id"]
        gmail.users().drafts().update(
            userId="me", id=gmail_draft_id, body=draft_payload
        ).execute()
        is_rev = True
    else:
        # Create new Gmail draft
        created = (
            gmail.users().drafts().create(userId="me", body=draft_payload).execute()
        )
        gmail_draft_id = created["id"]
        is_rev = False

    # Upsert SQLite approval record
    approval, _ = await upsert_email_approval(
        session_id=session_id,
        telegram_chat_id=telegram_chat_id,
        gmail_draft_id=gmail_draft_id,
        to_email=to_email,
        subject=subject,
        body=body,
    )

    action_str = "updated" if is_rev else "staged"
    return DraftResult(
        approval_id=approval.id,
        gmail_draft_id=gmail_draft_id,
        to_email=to_email,
        subject=subject,
        body=body,
        is_revision=is_rev,
        message=f"Draft successfully {action_str}. Reply YES-{approval.id} to send.",
    )
