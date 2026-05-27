class DomainError(Exception):
    """
    Domainの基底クラス
    """

class DomainValidationError(DomainError):
    """
    Doamin検証エラー。不正な値を受け取った場合などにエラーが発生する。
    """


class InfraError(Exception):
    """
    Infra層の基底エラー。
    """


class RuntimeResourceError(InfraError):
    """
    Runtime実行基盤のリソース操作に失敗した場合のエラー。
    """
