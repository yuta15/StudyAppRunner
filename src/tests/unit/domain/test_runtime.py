from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from src.app.domain.models.runtime import Runtime, RuntimeResourceId, RuntimeStatus
from src.app.exceptions import DomainValidationError


def test_new_success_create_runtime_with_default_state(runtime_default_ttl: timedelta) -> None:
    """Runtime.new() が新規 Runtime を CREATING 状態と 30 分後の期限で作成することを確認する。"""
    runtime = Runtime.new()

    assert isinstance(runtime.runtime_id, UUID)
    assert runtime.runtime_status == RuntimeStatus.CREATING
    assert runtime.expires_at == runtime.created_at + runtime_default_ttl
    assert runtime.created_at.tzinfo == timezone.utc
    assert runtime.runtime_resource_id is None


@pytest.mark.parametrize(
    ("expires_delta", "expected"),
    [
        (timedelta(seconds=-1), True),
        (timedelta(minutes=1), False),
    ],
)
def test_is_expired_success_return_expiration_result(
    runtime_factory: Callable[..., Runtime],
    expires_delta: timedelta,
    expected: bool,
) -> None:
    """expires_at が現在時刻を過ぎているかどうかで期限切れ判定が変わることを確認する。"""
    expires_at = datetime.now(tz=timezone.utc) + expires_delta
    runtime = runtime_factory(expires_at=expires_at)

    assert runtime.is_expired() is expected


def test_set_runtime_resource_id_success_accept_non_blank_value(
    runtime: Runtime,
    runtime_resource_id: RuntimeResourceId,
) -> None:
    """RuntimeResourceId を Runtime に設定できることを確認する。"""
    runtime.set_runtime_resource_id(runtime_resource_id)

    assert runtime.runtime_resource_id == runtime_resource_id


def test_runtime_resource_id_success_create_with_non_blank_value(runtime_resource_id_value: str) -> None:
    """空白のみではない値で RuntimeResourceId を作成できることを確認する。"""
    runtime_resource_id = RuntimeResourceId(runtime_resource_id_value)

    assert runtime_resource_id.value == runtime_resource_id_value


@pytest.mark.parametrize("runtime_resource_id", ["", " ", "  ", "\t", "\n"])
def test_runtime_resource_id_failure_reject_blank_value(runtime_resource_id: str) -> None:
    """空文字または空白のみの runtime_resource_id では RuntimeResourceId を作成できないことを確認する。"""
    with pytest.raises(DomainValidationError):
        RuntimeResourceId(runtime_resource_id)


@pytest.mark.parametrize(
    ("current_status", "transition", "expected_status"),
    [
        (RuntimeStatus.CREATING, "to_running", RuntimeStatus.RUNNING),
        (RuntimeStatus.STOPPED, "to_running", RuntimeStatus.RUNNING),
        (RuntimeStatus.RUNNING, "to_stopping", RuntimeStatus.STOPPING),
        (RuntimeStatus.STOPPING, "to_stopped", RuntimeStatus.STOPPED),
        (RuntimeStatus.CREATING, "to_failed", RuntimeStatus.FAILED),
        (RuntimeStatus.RUNNING, "to_expired", RuntimeStatus.EXPIRED),
    ],
)
def test_status_transition_success_update_runtime_status(
    runtime_factory: Callable[..., Runtime],
    current_status: RuntimeStatus,
    transition: str,
    expected_status: RuntimeStatus,
) -> None:
    """Runtime の状態遷移メソッドが許可された状態から期待する RuntimeStatus へ変更することを確認する。"""
    runtime = runtime_factory(runtime_status=current_status)

    getattr(runtime, transition)()

    assert runtime.runtime_status == expected_status


@pytest.mark.parametrize(
    ("current_status", "transition"),
    [
        (RuntimeStatus.FAILED, "to_running"),
        (RuntimeStatus.CREATING, "to_stopping"),
        (RuntimeStatus.RUNNING, "to_stopped"),
    ],
)
def test_status_transition_success_keep_status_when_transition_is_not_allowed(
    runtime_factory: Callable[..., Runtime],
    current_status: RuntimeStatus,
    transition: str,
) -> None:
    """許可されていない Runtime の状態遷移では現在の RuntimeStatus が維持されることを確認する。"""
    runtime = runtime_factory(runtime_status=current_status)

    getattr(runtime, transition)()

    assert runtime.runtime_status == current_status
