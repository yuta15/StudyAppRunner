from collections.abc import Callable
from uuid import uuid4

import pytest
from docker.client import DockerClient
from docker.errors import NotFound

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.infra.runtime.docker_runtime_adapter import DockerRuntimeAdapter

pytestmark = pytest.mark.integration


def test_create_and_remove_runtime_success_with_real_docker(
    real_docker_client: DockerClient,
    real_docker_runtime_adapter: DockerRuntimeAdapter,
    runtime_factory: Callable[..., Runtime],
) -> None:
    """
    実Docker daemonで Runtime 用コンテナを作成し、RuntimeResourceId で停止・削除できることを確認する。
    """
    runtime = runtime_factory(runtime_id=uuid4(), runtime_status=RuntimeStatus.CREATING)
    runtime_resource_id: RuntimeResourceId | None = None

    try:
        runtime_resource_id = real_docker_runtime_adapter.create_runtime(runtime)
        container = real_docker_client.containers.get(runtime_resource_id.value)
        container.reload()

        assert container.status == "running"
        assert container.labels["study_app.managed"] == "true"
        assert container.labels["study_app.runtime_id"] == str(runtime.runtime_id)

        real_docker_runtime_adapter.remove_runtime(runtime_resource_id)

        with pytest.raises(NotFound):
            real_docker_client.containers.get(runtime_resource_id.value)
    finally:
        if runtime_resource_id is not None:
            _remove_container_if_exists(
                docker_client=real_docker_client,
                runtime_resource_id=runtime_resource_id,
            )


def _remove_container_if_exists(
    docker_client: DockerClient,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    try:
        container = docker_client.containers.get(runtime_resource_id.value)
    except NotFound:
        return

    container.remove(force=True)
