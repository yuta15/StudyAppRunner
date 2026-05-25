from uuid import UUID
from abc import ABC, abstractmethod

from src.app.domain.models import Runtime


class RuntimePort(ABC):
    """
    暫定構成
    """
    @abstractmethod
    def create_runtime(self, runtime:Runtime) -> str:
        """
        Runtimeの作成・起動を実行する。
        暫定のため、引数は変わる可能性がある
        """
        pass

    @abstractmethod
    def remove_runtime(self, id:UUID) -> UUID:
        """
        Runtimeの停止・削除を実行する。
        暫定のため、引数は変わる可能性がある
        """
        pass