from uuid import UUID
from dataclasses import dataclass


@dataclass
class CreateRuntimeResponse:
    session_id:UUID
    runtime_id:UUID


@dataclass
class RemoveRuntimeResponse:
    runtime_id:UUID
