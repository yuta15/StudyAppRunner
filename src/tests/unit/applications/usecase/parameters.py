from datetime import datetime, timedelta, timezone
from uuid import UUID


DEFAULT_RUNTIME_ID = UUID("00000000-0000-0000-0000-000000000301")
DEFAULT_RUNTIME_CREATED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)
DEFAULT_RUNTIME_RESOURCE_ID = "container-1"
DEFAULT_RUNTIME_TTL = timedelta(minutes=30)
