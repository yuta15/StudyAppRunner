from collections.abc import Callable
from unittest.mock import MagicMock

import pytest

from src.app.applications.ports import RuntimePort
from src.app.applications.usecase.dependencies import RemoveRuntimeDependencies
from src.app.applications.usecase.remove_runtime import RemoveRuntime
from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.domain.repositories import RuntimeRepository
from src.app.exceptions import DomainValidationError, RuntimeResourceError


def test_exec_success_remove_runtime_resource_and_update_runtime_status(
    db_session_stub: object,
    runtime_factory: Callable[..., Runtime],
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """RUNNING の Runtime を STOPPING 保存後に削除し、STOPPED として保存することを確認する。"""
    runtime = runtime_factory(runtime_status=RuntimeStatus.RUNNING, runtime_resource_id=runtime_resource_id)
    runtime_repository = MagicMock(spec=RuntimeRepository)
    runtime_repository.get.return_value = runtime
    runtime_adapter = MagicMock(spec=RuntimePort)
    saved_statuses: list[RuntimeStatus] = []
    runtime_repository.save.side_effect = lambda runtime: saved_statuses.append(runtime.runtime_status)
    usecase = RemoveRuntime(
        session=db_session_stub,
        dependencies=RemoveRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
        ),
    )

    response = usecase.exec(runtime_id=runtime.runtime_id)

    runtime_repository.get.assert_called_once_with(runtime_id=runtime.runtime_id)
    runtime_adapter.remove_runtime.assert_called_once_with(runtime_resource_id=runtime_resource_id)
    assert saved_statuses == [RuntimeStatus.STOPPING, RuntimeStatus.STOPPED]
    assert response.runtime_id == runtime.runtime_id


def test_exec_success_remove_stopping_runtime_resource_and_update_runtime_status(
    db_session_stub: object,
    runtime_factory: Callable[..., Runtime],
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """STOPPING の Runtime を再実行で削除し、STOPPED として保存することを確認する。"""
    runtime = runtime_factory(runtime_status=RuntimeStatus.STOPPING, runtime_resource_id=runtime_resource_id)
    runtime_repository = MagicMock(spec=RuntimeRepository)
    runtime_repository.get.return_value = runtime
    runtime_adapter = MagicMock(spec=RuntimePort)
    saved_statuses: list[RuntimeStatus] = []
    runtime_repository.save.side_effect = lambda runtime: saved_statuses.append(runtime.runtime_status)
    usecase = RemoveRuntime(
        session=db_session_stub,
        dependencies=RemoveRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
        ),
    )

    response = usecase.exec(runtime_id=runtime.runtime_id)

    runtime_adapter.remove_runtime.assert_called_once_with(runtime_resource_id=runtime_resource_id)
    assert saved_statuses == [RuntimeStatus.STOPPED]
    assert response.runtime_id == runtime.runtime_id


def test_exec_failure_mark_runtime_failed_when_runtime_resource_removal_fails(
    db_session_stub: object,
    runtime_factory: Callable[..., Runtime],
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """Runtime リソース削除に失敗した場合に Runtime を FAILED として保存し、例外を再送出することを確認する。"""
    runtime = runtime_factory(runtime_status=RuntimeStatus.RUNNING, runtime_resource_id=runtime_resource_id)
    runtime_repository = MagicMock(spec=RuntimeRepository)
    runtime_repository.get.return_value = runtime
    runtime_adapter = MagicMock(spec=RuntimePort)
    runtime_adapter.remove_runtime.side_effect = RuntimeResourceError("failed to remove runtime resource")
    saved_statuses: list[RuntimeStatus] = []
    runtime_repository.save.side_effect = lambda runtime: saved_statuses.append(runtime.runtime_status)
    usecase = RemoveRuntime(
        session=db_session_stub,
        dependencies=RemoveRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
        ),
    )

    with pytest.raises(RuntimeResourceError):
        usecase.exec(runtime_id=runtime.runtime_id)

    runtime_adapter.remove_runtime.assert_called_once_with(runtime_resource_id=runtime_resource_id)
    assert saved_statuses == [RuntimeStatus.STOPPING, RuntimeStatus.FAILED]


def test_exec_failure_reject_runtime_without_runtime_resource_id(
    db_session_stub: object,
    runtime_factory: Callable[..., Runtime],
) -> None:
    """runtime_resource_id を持たない Runtime では Runtime リソース削除を実行しないことを確認する。"""
    runtime = runtime_factory(runtime_status=RuntimeStatus.RUNNING)
    runtime_repository = MagicMock(spec=RuntimeRepository)
    runtime_repository.get.return_value = runtime
    runtime_adapter = MagicMock(spec=RuntimePort)
    usecase = RemoveRuntime(
        session=db_session_stub,
        dependencies=RemoveRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
        ),
    )

    with pytest.raises(DomainValidationError):
        usecase.exec(runtime_id=runtime.runtime_id)

    runtime_adapter.remove_runtime.assert_not_called()
    runtime_repository.save.assert_not_called()


def test_exec_failure_reject_runtime_that_is_not_running(
    db_session_stub: object,
    runtime_factory: Callable[..., Runtime],
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """RUNNING ではない Runtime では Runtime リソース削除を実行しないことを確認する。"""
    runtime = runtime_factory(runtime_status=RuntimeStatus.STOPPED, runtime_resource_id=runtime_resource_id)
    runtime_repository = MagicMock(spec=RuntimeRepository)
    runtime_repository.get.return_value = runtime
    runtime_adapter = MagicMock(spec=RuntimePort)
    usecase = RemoveRuntime(
        session=db_session_stub,
        dependencies=RemoveRuntimeDependencies(
            runtime_adapter=runtime_adapter,
            runtime_repository=runtime_repository,
        ),
    )

    with pytest.raises(DomainValidationError):
        usecase.exec(runtime_id=runtime.runtime_id)

    runtime_adapter.remove_runtime.assert_not_called()
    runtime_repository.save.assert_not_called()
