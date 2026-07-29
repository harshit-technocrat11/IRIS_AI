from app.models.email_models import EmailContent, EmailSummary, _get_google_services
from agents import function_tool
import base64
import re

@function_tool
async def read_thread(message_id: str) -> EmailContent:
    """Retrieves full plain-text email body content by message or thread ID."""
    gmail, _ = _get_google_services()
    msg = (
        gmail.users()
        .messages()
        .get(userId="me", id=message_id, format="full")
        .execute()
    )

    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

    body = ""
    payload = msg.get("payload", {})
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                body = base64.urlsafe_b64decode(data).decode("utf-8")
                break
    else:
        data = payload.get("body", {}).get("data", "")
        body = base64.urlsafe_b64decode(data).decode("utf-8")


    response = EmailContent(
        id=msg["id"],
        thread_id=msg["threadId"],
        sender=headers.get("From", "Unknown"),
        recipients=headers.get("To", "Unknown"),
        subject=headers.get("Subject", "No Subject"),
        body=body,
        date=headers.get("Date", ""),
    )
    
    print( "email-content retrieved:", response)

    return response
