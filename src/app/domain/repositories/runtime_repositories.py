from uuid import UUID
from abc import ABC, abstractmethod

from src.app.domain.models import Runtime


class RuntimeRepository(ABC):
    @abstractmethod
    def save(self, runtime:Runtime) -> None:...

    @abstractmethod
    def get(self, runtime_id:UUID) -> Runtime:...
