from pydantic import BaseModel, Field
from typing import Optional, List
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class EmailSummary(BaseModel):
    id: str
    sender: str
    subject: str
    snippet: str
    date: str


class EmailContent(BaseModel):
    id: str
    thread_id: str
    sender: str
    recipients: str
    subject: str
    body: str
    date: str


class DraftPreview(BaseModel):
    approval_id: str
    gmail_draft_id: str
    resolved_email: str
    subject: str
    body: str
    is_updated_draft: bool

class ContactResolutionResult(BaseModel):
    status: str = Field(description="'MATCH_FOUND', 'AMBIGUOUS', or 'NOT_FOUND'")
    matched_email: Optional[str] = Field(default=None)
    candidates: List[str] = Field(default_factory=list)
    message: str


class DraftResult(BaseModel):
    approval_id: str
    gmail_draft_id: str
    to_email: str
    subject: str
    body: str
    is_revision: bool
    message: str


def _get_google_services():
    creds = Credentials.from_authorized_user_file("token.json")
    gmail = build("gmail", "v1", credentials=creds)
    people = build("people", "v1", credentials=creds)
    return gmail, people
