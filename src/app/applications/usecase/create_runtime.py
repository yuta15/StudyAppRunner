from sqlmodel import Session as DBSession

from src.app.applications.usecase.dependencies import CreateRuntimeDependencies
from src.app.applications.usecase.dto import CreateRuntimeResponse
from src.app.domain.models import Session, Runtime


class CreateRuntime:
    def __init__(self, session:DBSession, dependencies:CreateRuntimeDependencies):
        self._dependencies = dependencies
        self._session = session

    def exec(self) -> CreateRuntimeResponse:
        runtime = Runtime.new()
        session = Session.new(runtime_id=runtime.runtime_id)

        with self._session.begin():
            self._dependencies.runtime_repository.save(runtime=runtime)
            self._dependencies.session_repository.save(session=session)

        try:
            runtime_resource_id = self._dependencies.runtime_adapter.create_runtime(runtime=runtime)
        except Exception:
            runtime.to_failed()
            raise
        else:
            runtime.set_runtime_resource_id(runtime_resource_id=runtime_resource_id)
            runtime.to_running()

        with self._session.begin():
            self._dependencies.runtime_repository.save(runtime=runtime)

        return CreateRuntimeResponse(session_id=session.session_id, runtime_id=runtime.runtime_id)