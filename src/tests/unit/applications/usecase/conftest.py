from collections.abc import Callable
from contextlib import nullcontext
from datetime import datetime
from uuid import UUID

import pytest

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.tests.unit.applications.usecase.parameters import (
    DEFAULT_RUNTIME_CREATED_AT,
    DEFAULT_RUNTIME_ID,
    DEFAULT_RUNTIME_RESOURCE_ID,
    DEFAULT_RUNTIME_TTL,
)


class DBSessionStub:
    def begin(self) -> nullcontext[None]:
        return nullcontext()


@pytest.fixture
def db_session_stub() -> DBSessionStub:
    return DBSessionStub()


@pytest.fixture
def runtime_resource_id() -> RuntimeResourceId:
    return RuntimeResourceId(DEFAULT_RUNTIME_RESOURCE_ID)


@pytest.fixture
def runtime_factory() -> Callable[..., Runtime]:
    def _factory(
        *,
        runtime_id: UUID = DEFAULT_RUNTIME_ID,
        runtime_status: RuntimeStatus = RuntimeStatus.CREATING,
        created_at: datetime = DEFAULT_RUNTIME_CREATED_AT,
        expires_at: datetime | None = None,
        runtime_resource_id: RuntimeResourceId | None = None,
    ) -> Runtime:
        return Runtime(
            runtime_id=runtime_id,
            runtime_status=runtime_status,
            created_at=created_at,
            expires_at=expires_at or created_at + DEFAULT_RUNTIME_TTL,
            runtime_resource_id=runtime_resource_id,
        )

    return _factory
