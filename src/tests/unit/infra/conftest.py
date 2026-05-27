from collections.abc import Callable
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from docker.errors import APIError, NotFound

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.exceptions import RuntimeResourceError
from src.app.infra.runtime.docker_runtime_adapter import DockerRuntimeAdapter
from src.tests.unit.infra.parameters import (
    DEFAULT_DOCKER_COMMAND,
    DEFAULT_DOCKER_IMAGE,
    DEFAULT_DOCKER_WORKING_DIR,
    DEFAULT_RUNTIME_CREATED_AT,
    DEFAULT_RUNTIME_ID,
    DEFAULT_RUNTIME_RESOURCE_ID,
    DEFAULT_RUNTIME_TTL,
)


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


@pytest.fixture
def runtime(runtime_factory: Callable[..., Runtime]) -> Runtime:
    return runtime_factory()


@pytest.fixture
def runtime_resource_id_value() -> str:
    return DEFAULT_RUNTIME_RESOURCE_ID


@pytest.fixture
def runtime_resource_id(runtime_resource_id_value: str) -> RuntimeResourceId:
    return RuntimeResourceId(runtime_resource_id_value)


@pytest.fixture
def docker_image() -> str:
    return DEFAULT_DOCKER_IMAGE


@pytest.fixture
def docker_command() -> str:
    return DEFAULT_DOCKER_COMMAND


@pytest.fixture
def docker_working_dir() -> str:
    return DEFAULT_DOCKER_WORKING_DIR


@pytest.fixture
def docker_container_name(runtime: Runtime) -> str:
    return f"studyapp-runtime-{runtime.runtime_id}"


@pytest.fixture
def docker_labels(runtime: Runtime) -> dict[str, str]:
    return {
        "study_app.managed": "true",
        "study_app.runtime_id": str(runtime.runtime_id),
    }


@pytest.fixture
def docker_create_container_kwargs(
    docker_command: str,
    docker_container_name: str,
    docker_image: str,
    docker_labels: dict[str, str],
    docker_working_dir: str,
) -> dict[str, object]:
    return {
        "image": docker_image,
        "command": docker_command,
        "working_dir": docker_working_dir,
        "name": docker_container_name,
        "detach": True,
        "tty": True,
        "stdin_open": True,
        "labels": docker_labels,
    }


@pytest.fixture
def docker_container(runtime_resource_id_value: str) -> MagicMock:
    container = MagicMock()
    container.id = runtime_resource_id_value
    return container


@pytest.fixture
def docker_client(docker_container: MagicMock) -> MagicMock:
    client = MagicMock()
    client.containers.run.return_value = docker_container
    client.containers.get.return_value = docker_container
    return client


@pytest.fixture
def docker_api_error() -> APIError:
    return APIError("docker api failed")


@pytest.fixture
def docker_not_found_error() -> NotFound:
    return NotFound("container not found")


@pytest.fixture
def runtime_resource_error() -> type[RuntimeResourceError]:
    return RuntimeResourceError


@pytest.fixture
def docker_runtime_adapter(
    docker_client: MagicMock,
    docker_command: str,
    docker_image: str,
    docker_working_dir: str,
) -> DockerRuntimeAdapter:
    return DockerRuntimeAdapter(
        docker_client=docker_client,
        image=docker_image,
        command=docker_command,
        working_dir=docker_working_dir,
    )
