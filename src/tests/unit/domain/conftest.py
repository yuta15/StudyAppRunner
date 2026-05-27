from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.domain.models.session import Session, SessionStatus
from src.tests.unit.domain.parameters import (
    DEFAULT_RUNTIME_ID,
    DEFAULT_RUNTIME_RESOURCE_ID,
    DEFAULT_RUNTIME_TTL,
    DEFAULT_SESSION_ID,
    DEFAULT_SESSION_RUNTIME_ID,
)


@pytest.fixture
def runtime_default_ttl() -> timedelta:
    return DEFAULT_RUNTIME_TTL


@pytest.fixture
def runtime_resource_id_value() -> str:
    return DEFAULT_RUNTIME_RESOURCE_ID


@pytest.fixture
def runtime_resource_id(runtime_resource_id_value: str) -> RuntimeResourceId:
    return RuntimeResourceId(runtime_resource_id_value)


@pytest.fixture
def session_runtime_id() -> UUID:
    return DEFAULT_SESSION_RUNTIME_ID


@pytest.fixture
def runtime_factory() -> Callable[..., Runtime]:
    def _factory(
        *,
        runtime_id: UUID = DEFAULT_RUNTIME_ID,
        runtime_status: RuntimeStatus = RuntimeStatus.CREATING,
        created_at: datetime | None = None,
        expires_at: datetime | None = None,
        runtime_resource_id: RuntimeResourceId | None = None,
    ) -> Runtime:
        created_at = created_at or datetime.now(tz=timezone.utc)
        return Runtime(
            runtime_id=runtime_id,
            runtime_status=runtime_status,
            created_at=created_at,
            expires_at=expires_at or created_at + DEFAULT_RUNTIME_TTL,
            runtime_resource_id=runtime_resource_id,
        )

    return _factory


@pytest.fixture
def runtime(runtime_factory: Callable[..., Runtime]) -> Runtime:
    return runtime_factory()


@pytest.fixture
def session_factory() -> Callable[..., Session]:
    def _factory(
        *,
        session_id: UUID = DEFAULT_SESSION_ID,
        runtime_id: UUID = DEFAULT_SESSION_RUNTIME_ID,
        session_status: SessionStatus = SessionStatus.ACTIVE,
        activated_at: datetime | None = None,
        inactivated_at: datetime | None = None,
        expired_at: datetime | None = None,
    ) -> Session:
        return Session(
            session_id=session_id,
            runtime_id=runtime_id,
            session_status=session_status,
            activated_at=activated_at or datetime.now(tz=timezone.utc),
            inactivated_at=inactivated_at,
            expired_at=expired_at,
        )

    return _factory


@pytest.fixture
def active_session(session_factory: Callable[..., Session]) -> Session:
    return session_factory()
