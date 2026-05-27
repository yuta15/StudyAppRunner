from typing import Protocol

from docker.errors import DockerException, NotFound

from src.app.applications.ports import RuntimePort
from src.app.domain.models import Runtime, RuntimeResourceId
from src.app.exceptions import DomainValidationError, RuntimeResourceError


class _DockerContainer(Protocol):
    id: str

    def stop(self) -> None: ...

    def remove(self) -> None: ...


class _DockerContainerCollection(Protocol):
    def run(self, **kwargs: object) -> _DockerContainer: ...

    def get(self, container_id: str) -> _DockerContainer: ...


class _DockerClient(Protocol):
    containers: _DockerContainerCollection


class DockerRuntimeAdapter(RuntimePort):
    """
    Dockerを使ってRuntime実行リソースを作成・削除するAdapter。
    """

    def __init__(
        self,
        docker_client: _DockerClient,
        image: str,
        command: str,
        working_dir: str,
    ) -> None:
        self._docker_client = docker_client
        self._image = image
        self._command = command
        self._working_dir = working_dir

    def create_runtime(self, runtime: Runtime) -> RuntimeResourceId:
        """
        Dockerコンテナを作成・起動し、コンテナIDを返す。
        """
        try:
            container = self._docker_client.containers.run(
                image=self._image,
                command=self._command,
                working_dir=self._working_dir,
                name=self._container_name(runtime=runtime),
                detach=True,
                tty=True,
                stdin_open=True,
                labels=self._labels(runtime=runtime),
            )
        except DockerException as error:
            raise RuntimeResourceError("failed to create runtime resource") from error

        try:
            return RuntimeResourceId(container.id)
        except DomainValidationError as error:
            raise RuntimeResourceError("created runtime resource id is invalid") from error

    def remove_runtime(self, runtime_resource_id: RuntimeResourceId) -> None:
        """
        Dockerコンテナを停止・削除する。
        """
        try:
            container = self._docker_client.containers.get(runtime_resource_id.value)
            container.stop()
            container.remove()
        except NotFound:
            return
        except DockerException as error:
            raise RuntimeResourceError("failed to remove runtime resource") from error

    def _container_name(self, runtime: Runtime) -> str:
        return f"studyapp-runtime-{runtime.runtime_id}"

    def _labels(self, runtime: Runtime) -> dict[str, str]:
        return {
            "study_app.managed": "true",
            "study_app.runtime_id": str(runtime.runtime_id),
        }
