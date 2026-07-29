
import enum
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from sqlmodel import SQLModel, Field, Column, JSON


class ActionType(str, enum.Enum):
    SEND_EMAIL = "send_email"
    CREATE_EVENT = "create_event"


class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class PendingApproval(SQLModel, table=True):
    __tablename__ = "pending_approvals"

    id: str = Field(
        default_factory=lambda: secrets.token_hex(2).upper(),
        primary_key=True,
        index=True,
        max_length=10,
    )
    action_type: ActionType = Field(default=ActionType.SEND_EMAIL, index=True)

    payload: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    status: ApprovalStatus = Field(default=ApprovalStatus.PENDING, index=True)
    telegram_chat_id: int = Field(index=True)
    session_id: str = Field(index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=30)
    )
