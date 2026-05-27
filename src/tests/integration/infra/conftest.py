from collections.abc import Callable, Iterator
from datetime import datetime
from uuid import UUID

import docker
import pytest
from docker.client import DockerClient
from docker.errors import DockerException, NotFound

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.infra.runtime.docker_runtime_adapter import DockerRuntimeAdapter
from src.tests.integration.infra.parameters import (
    DEFAULT_RUNTIME_CREATED_AT,
    DEFAULT_RUNTIME_ID,
    DEFAULT_RUNTIME_TTL,
    INTEGRATION_DOCKER_COMMAND,
    INTEGRATION_DOCKER_IMAGE,
    INTEGRATION_DOCKER_WORKING_DIR,
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


@pytest.fixture(scope="session")
def real_docker_client() -> Iterator[DockerClient]:
    try:
        client = docker.from_env()
        client.ping()
    except DockerException as error:
        pytest.skip(f"Docker daemon is not available: {error}")

    yield client
    client.close()


@pytest.fixture(scope="session")
def integration_docker_image(real_docker_client: DockerClient) -> str:
    try:
        real_docker_client.images.get(INTEGRATION_DOCKER_IMAGE)
    except NotFound:
        pytest.skip(f"Docker image {INTEGRATION_DOCKER_IMAGE} is not available locally")
    except DockerException as error:
        pytest.skip(f"Docker image {INTEGRATION_DOCKER_IMAGE} is not available: {error}")

    return INTEGRATION_DOCKER_IMAGE


@pytest.fixture(scope="session")
def integration_docker_command() -> str:
    return INTEGRATION_DOCKER_COMMAND


@pytest.fixture(scope="session")
def integration_docker_working_dir() -> str:
    return INTEGRATION_DOCKER_WORKING_DIR


@pytest.fixture
def real_docker_runtime_adapter(
    integration_docker_command: str,
    integration_docker_image: str,
    integration_docker_working_dir: str,
    real_docker_client: DockerClient,
) -> DockerRuntimeAdapter:
    return DockerRuntimeAdapter(
        docker_client=real_docker_client,
        image=integration_docker_image,
        command=integration_docker_command,
        working_dir=integration_docker_working_dir,
    )
