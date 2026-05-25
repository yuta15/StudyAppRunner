from uuid import UUID
from abc import ABC, abstractmethod

from src.app.domain.models import Session


class SessionRepository(ABC):
    @abstractmethod
    def save(self, session:Session) -> None:...

    @abstractmethod
    def get(self, session_id:UUID) -> Session:...
