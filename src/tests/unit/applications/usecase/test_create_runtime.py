from unittest.mock import MagicMock

import pytest

from src.app.applications.ports import RuntimePort
from src.app.applications.usecase.create_runtime import CreateRuntime
from src.app.applications.usecase.dependencies import CreateRuntimeDependencies
from src.app.domain.models import Runtime, Session
from src.app.domain.models.runtime import RuntimeResourceId, RuntimeStatus
from src.app.domain.models.session import SessionStatus
from src.app.domain.repositories import RuntimeRepository, SessionRepository


def test_exec_failure_remove_runtime_resource_when_runtime_save_fails_after_resource_creation(
    db_session_stub: object,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """Runtime リソース作成後の Runtime 保存に失敗した場合に作成済みリソースを削除することを確認する。"""
    save_error = RuntimeError("failed to save runtime")
    runtime_repository = MagicMock(spec=RuntimeRepository)
    session_repository = MagicMock(spec=SessionRepository)
    runtime_adapter = MagicMock(spec=RuntimePort)
    runtime_adapter.create_runtime.return_value = runtime_resource_id
    saved_runtime_statuses: list[RuntimeStatus] = []
    saved_session_statuses: list[SessionStatus] = []

    def save_runtime(runtime: Runtime) -> None:
        saved_runtime_statuses.append(runtime.runtime_status)
        if runtime.runtime_status == RuntimeStatus.RUNNING:
            raise save_error

    def save_session(session: Session) -> None:
        saved_session_statuses.append(session.session_status)

    runtime_repository.save.side_effect = save_runtime
    session_repository.save.side_effect = save_session
    usecase = CreateRuntime(
        session=db_session_stub,
        dependencies=CreateRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
            session_repository=session_repository,
        ),
    )

    with pytest.raises(RuntimeError):
        usecase.exec()

    runtime_adapter.remove_runtime.assert_called_once_with(runtime_resource_id=runtime_resource_id)
    assert saved_runtime_statuses == [RuntimeStatus.CREATING, RuntimeStatus.RUNNING, RuntimeStatus.FAILED]
    assert saved_session_statuses == [SessionStatus.ACTIVE, SessionStatus.INACTIVE]
