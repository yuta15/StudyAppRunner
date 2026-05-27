from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Self

from src.app.domain.models.runtime.entities.runtime_resource_id import RuntimeResourceId
from src.app.domain.models.runtime.enum import RuntimeStatus


@dataclass
class Runtime:
    runtime_id:UUID
    runtime_status:RuntimeStatus
    created_at:datetime
    expires_at:datetime
    runtime_resource_id:RuntimeResourceId | None = None

    @classmethod
    def new(cls) -> Self:
        utc_now = datetime.now(tz=timezone.utc)
        return Runtime(
            runtime_id=uuid4(),
            runtime_status=RuntimeStatus.CREATING,
            created_at=utc_now,
            expires_at=utc_now + timedelta(minutes=30)
        )

    def set_runtime_resource_id(self, runtime_resource_id:RuntimeResourceId) -> None:
        self.runtime_resource_id = runtime_resource_id

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(tz=timezone.utc)
    
    def to_running(self) -> None:
        allowed_status = [RuntimeStatus.CREATING, RuntimeStatus.STOPPED]
        if self.runtime_status in allowed_status:
            self.runtime_status = RuntimeStatus.RUNNING

    def to_stopping(self) -> None:
        if self.runtime_status == RuntimeStatus.RUNNING:
            self.runtime_status = RuntimeStatus.STOPPING

    def to_stopped(self) -> None:
        if self.runtime_status == RuntimeStatus.STOPPING:
            self.runtime_status = RuntimeStatus.STOPPED

    def to_failed(self) -> None:
        if self.runtime_status != RuntimeStatus.FAILED:
            self.runtime_status = RuntimeStatus.FAILED

    def to_expired(self) -> None:
        if self.runtime_status != RuntimeStatus.EXPIRED:
            self.runtime_status = RuntimeStatus.EXPIRED
