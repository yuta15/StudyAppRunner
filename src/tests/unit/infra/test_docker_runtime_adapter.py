from unittest.mock import MagicMock, call

import pytest

from src.app.domain.models.runtime import Runtime, RuntimeResourceId


def test_create_runtime_success_create_started_container_and_return_resource_id(
    docker_client: MagicMock,
    docker_create_container_kwargs: dict[str, object],
    docker_runtime_adapter: object,
    runtime: Runtime,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """Docker 実装が Runtime 作成用の設定と label でコンテナを作成・起動し、コンテナ ID を返すことを確認する。"""
    created_runtime_resource_id = docker_runtime_adapter.create_runtime(runtime)

    docker_client.containers.run.assert_called_once_with(**docker_create_container_kwargs)
    assert created_runtime_resource_id == runtime_resource_id


def test_create_runtime_failure_raise_runtime_resource_error_when_docker_api_fails(
    docker_api_error: Exception,
    docker_client: MagicMock,
    docker_runtime_adapter: object,
    runtime: Runtime,
    runtime_resource_error: type[Exception],
) -> None:
    """Docker API が失敗した場合に Runtime 作成失敗として扱える例外を送出することを確認する。"""
    docker_client.containers.run.side_effect = docker_api_error

    with pytest.raises(runtime_resource_error):
        docker_runtime_adapter.create_runtime(runtime)


def test_remove_runtime_success_stop_and_remove_container_by_runtime_resource_id(
    docker_client: MagicMock,
    docker_container: MagicMock,
    docker_runtime_adapter: object,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """Docker 実装が runtime_resource_id で対象コンテナを取得し、停止・削除することを確認する。"""
    docker_runtime_adapter.remove_runtime(runtime_resource_id)

    docker_client.containers.get.assert_called_once_with(runtime_resource_id.value)
    assert docker_container.method_calls == [call.stop(), call.remove()]


def test_remove_runtime_success_ignore_missing_container(
    docker_client: MagicMock,
    docker_not_found_error: Exception,
    docker_runtime_adapter: object,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """削除対象のコンテナが存在しない場合でも削除済みとして正常終了することを確認する。"""
    docker_client.containers.get.side_effect = docker_not_found_error

    docker_runtime_adapter.remove_runtime(runtime_resource_id)

    docker_client.containers.get.assert_called_once_with(runtime_resource_id.value)


@pytest.mark.parametrize("failed_operation", ["get", "stop", "remove"])
def test_remove_runtime_failure_raise_runtime_resource_error_when_docker_api_fails(
    docker_api_error: Exception,
    docker_client: MagicMock,
    docker_container: MagicMock,
    docker_runtime_adapter: object,
    failed_operation: str,
    runtime_resource_error: type[Exception],
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """Docker API が失敗した場合に Runtime 削除失敗として扱える例外を送出することを確認する。"""
    if failed_operation == "get":
        docker_client.containers.get.side_effect = docker_api_error
    elif failed_operation == "stop":
        docker_container.stop.side_effect = docker_api_error
    else:
        docker_container.remove.side_effect = docker_api_error

    with pytest.raises(runtime_resource_error):
        docker_runtime_adapter.remove_runtime(runtime_resource_id)
