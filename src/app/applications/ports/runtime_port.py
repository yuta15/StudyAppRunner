from abc import ABC, abstractmethod

from src.app.domain.models import Runtime, RuntimeResourceId


class RuntimePort(ABC):
    """
    暫定構成
    """
    @abstractmethod
    def create_runtime(self, runtime:Runtime) -> RuntimeResourceId:
        """
        Runtimeの作成・起動を実行する。
        作成した実行基盤のリソースIDをRuntimeResourceIdとして返す。
        暫定のため、引数は変わる可能性がある
        """
        pass

    @abstractmethod
    def remove_runtime(self, runtime_resource_id:RuntimeResourceId) -> None:
        """
        Runtimeの停止・削除を実行する。
        RuntimeResourceIdを指定して削除し、戻り値は返さない。
        暫定のため、引数は変わる可能性がある
        """
        pass
