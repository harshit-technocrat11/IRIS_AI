from app.models.email_models import (EmailContent, EmailSummary, _get_google_services)
from agents import function_tool
from typing import List, Optional


@function_tool
async def search_emails(query: str, max_results: int = 5) -> List[EmailSummary]:
    """Search Gmail inbox using standard search queries. Returns metadata summaries only."""
    gmail, _ = _get_google_services()
    results = (
        gmail.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    messages = results.get("messages", [])

    summaries = []
    for msg in messages:
        msg_detail = (
            gmail.users()
            .messages()
            .get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
            .execute()
        )

        headers = {
            h["name"]: h["value"]
            for h in msg_detail.get("payload", {}).get("headers", [])
        }
        summaries.append(
            EmailSummary(
                id=msg["id"],
                sender=headers.get("From", "Unknown"),
                subject=headers.get("Subject", "No Subject"),
                snippet=msg_detail.get("snippet", ""),
                date=headers.get("Date", ""),
            )
        )

        print("emails search tool: ", summaries)

    return summaries


