from datetime import datetime, timezone 
from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Self

from src.app.domain.models.session.enum import SessionStatus


@dataclass
class Session:
    session_id:UUID
    runtime_id:UUID
    session_status: SessionStatus
    activated_at:datetime
    inactivated_at:datetime | None = None
    expired_at:datetime | None = None

    @classmethod
    def new(cls, runtime_id:UUID) -> Self:
        return Session(
            session_id=uuid4(),
            session_status=SessionStatus.ACTIVE,
            runtime_id=runtime_id,
            activated_at=datetime.now(tz=timezone.utc))

    def to_inactive(self) -> None:
        if self.session_status == SessionStatus.ACTIVE:
            self.session_status = SessionStatus.INACTIVE
            self.inactivated_at = datetime.now(tz=timezone.utc)

    def to_expired(self) -> None:
        if self.session_status == SessionStatus.ACTIVE:
            self.session_status = SessionStatus.EXPIRED
            self.expired_at = datetime.now(tz=timezone.utc)