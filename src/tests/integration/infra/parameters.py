from datetime import datetime, timedelta, timezone
from uuid import UUID


DEFAULT_RUNTIME_ID = UUID("00000000-0000-0000-0000-000000000201")
DEFAULT_RUNTIME_CREATED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)
DEFAULT_RUNTIME_TTL = timedelta(minutes=30)

INTEGRATION_DOCKER_IMAGE = "busybox:1.36.1"
INTEGRATION_DOCKER_COMMAND = "/bin/sh"
INTEGRATION_DOCKER_WORKING_DIR = "/workspace"
