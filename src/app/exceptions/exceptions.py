class DomainError(Exception):
    """
    Domainの基底クラス
    """

class DomainValidationError(DomainError):
    """
    Doamin検証エラー。不正な値を受け取った場合などにエラーが発生する。
    """
