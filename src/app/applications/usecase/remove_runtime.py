from uuid import UUID

from sqlmodel import Session as DBSession

from src.app.applications.usecase.dependencies import RemoveRuntimeDependencies
from src.app.applications.usecase.dto import RemoveRuntimeResponse
from src.app.domain.models import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.exceptions import DomainValidationError


class RemoveRuntime:
    def __init__(self, session: DBSession, dependencies: RemoveRuntimeDependencies):
        self._dependencies = dependencies
        self._session = session

    def exec(self, runtime_id: UUID) -> RemoveRuntimeResponse:
        runtime = self._dependencies.runtime_repository.get(runtime_id=runtime_id)
        runtime_resource_id = self._runtime_resource_id(runtime=runtime)

        self._start_runtime_removal(runtime=runtime)

        try:
            self._dependencies.runtime_adapter.remove_runtime(runtime_resource_id=runtime_resource_id)
        except Exception:
            self._fail_runtime_removal(runtime=runtime)
            raise

        runtime.to_stopped()
        self._save_runtime(runtime=runtime)

        return RemoveRuntimeResponse(runtime_id=runtime.runtime_id)

    def _runtime_resource_id(self, runtime: Runtime) -> RuntimeResourceId:
        if runtime.runtime_resource_id is None:
            raise DomainValidationError("runtime resource id is not set")
        return runtime.runtime_resource_id

    def _start_runtime_removal(self, runtime: Runtime) -> None:
        if runtime.runtime_status != RuntimeStatus.RUNNING:
            raise DomainValidationError("runtime is not running")

        runtime.to_stopping()
        self._save_runtime(runtime=runtime)

    def _fail_runtime_removal(self, runtime: Runtime) -> None:
        runtime.to_failed()
        self._save_runtime(runtime=runtime)

    def _save_runtime(self, runtime: Runtime) -> None:
        with self._session.begin():
            self._dependencies.runtime_repository.save(runtime=runtime)
