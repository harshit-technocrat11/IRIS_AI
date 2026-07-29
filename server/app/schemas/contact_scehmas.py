# app/models/contact_schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactProfile(BaseModel):
    name: str = Field(description="Full name of the contact")
    emails: List[str] = Field(
        default_factory=list, description="Associated email addresses"
    )
    phones: List[str] = Field(
        default_factory=list, description="Associated phone numbers if available"
    )
    job_title: Optional[str] = Field(
        default=None, description="Job title or organization role"
    )
    source: str = Field(
        description="Source of data: 'Google Contacts' or 'Email History'"
    )


class ContactSearchResult(BaseModel):
    query: str
    total_found: int
    contacts: List[ContactProfile] = Field(default_factory=list)
    message: str
