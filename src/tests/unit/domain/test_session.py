from collections.abc import Callable
from datetime import datetime, timezone
from uuid import UUID

from src.app.domain.models.session import Session, SessionStatus


def test_new_success_create_session_with_default_state(session_runtime_id: UUID) -> None:
    """Session.new() が Runtime に紐づく ACTIVE 状態の Session を作成することを確認する。"""
    session = Session.new(runtime_id=session_runtime_id)

    assert isinstance(session.session_id, UUID)
    assert session.runtime_id == session_runtime_id
    assert session.session_status == SessionStatus.ACTIVE
    assert session.activated_at.tzinfo == timezone.utc
    assert session.inactivated_at is None
    assert session.expired_at is None


def test_to_inactive_success_update_active_session_to_inactive(active_session: Session) -> None:
    """ACTIVE 状態の Session を INACTIVE に変更し、非アクティブ化時刻を記録することを確認する。"""
    session_id = active_session.session_id
    runtime_id = active_session.runtime_id

    active_session.to_inactive()

    assert active_session.session_status == SessionStatus.INACTIVE
    assert isinstance(active_session.inactivated_at, datetime)
    assert active_session.expired_at is None
    assert active_session.session_id == session_id
    assert active_session.runtime_id == runtime_id


def test_to_expired_success_update_active_session_to_expired(active_session: Session) -> None:
    """ACTIVE 状態の Session を EXPIRED に変更し、期限切れ時刻を記録することを確認する。"""
    session_id = active_session.session_id
    runtime_id = active_session.runtime_id

    active_session.to_expired()

    assert active_session.session_status == SessionStatus.EXPIRED
    assert isinstance(active_session.expired_at, datetime)
    assert active_session.inactivated_at is None
    assert active_session.session_id == session_id
    assert active_session.runtime_id == runtime_id


def test_to_expired_success_keep_inactive_session(session_factory: Callable[..., Session]) -> None:
    """INACTIVE 状態の Session に期限切れ操作をしても状態と期限切れ時刻が変わらないことを確認する。"""
    inactivated_at = datetime.now(tz=timezone.utc)
    session = session_factory(session_status=SessionStatus.INACTIVE, inactivated_at=inactivated_at)

    session.to_expired()

    assert session.session_status == SessionStatus.INACTIVE
    assert session.inactivated_at == inactivated_at
    assert session.expired_at is None
