from sqlmodel import Session as DBSession

from src.app.applications.usecase.dependencies import CreateRuntimeDependencies
from src.app.applications.usecase.dto import CreateRuntimeResponse
from src.app.domain.models import Session, Runtime


class CreateRuntime:
    def __init__(self, session: DBSession, dependencies: CreateRuntimeDependencies):
        self._dependencies = dependencies
        self._session = session

    def exec(self) -> CreateRuntimeResponse:
        runtime = Runtime.new()
        session = Session.new(runtime_id=runtime.runtime_id)

        self._save_runtime_and_session(runtime=runtime, session=session)

        try:
            self._create_runtime_resource(runtime=runtime)
        except Exception:
            self._fail_runtime_creation(runtime=runtime, session=session)
            raise

        self._save_runtime(runtime=runtime)

        return CreateRuntimeResponse(session_id=session.session_id, runtime_id=runtime.runtime_id)

    def _create_runtime_resource(self, runtime: Runtime) -> None:
        runtime_resource_id = self._dependencies.runtime_adapter.create_runtime(runtime=runtime)
        runtime.set_runtime_resource_id(runtime_resource_id=runtime_resource_id)
        runtime.to_running()

    def _fail_runtime_creation(self, runtime: Runtime, session: Session) -> None:
        runtime.to_failed()
        session.to_inactive()
        self._save_runtime_and_session(runtime=runtime, session=session)

    def _save_runtime(self, runtime: Runtime) -> None:
        with self._session.begin():
            self._dependencies.runtime_repository.save(runtime=runtime)

    def _save_runtime_and_session(self, runtime: Runtime, session: Session) -> None:
        with self._session.begin():
            self._dependencies.runtime_repository.save(runtime=runtime)
            self._dependencies.session_repository.save(session=session)
