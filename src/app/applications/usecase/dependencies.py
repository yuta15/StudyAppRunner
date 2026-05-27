from dataclasses import dataclass

from src.app.applications.ports import RuntimePort
from src.app.domain.repositories import RuntimeRepository, SessionRepository


@dataclass
class CreateRuntimeDependencies:
    runtime_adapter: RuntimePort
    runtime_repository: RuntimeRepository
    session_repository: SessionRepository


@dataclass
class RemoveRuntimeDependencies:
    runtime_adapter: RuntimePort
    runtime_repository: RuntimeRepository
