from dataclasses import dataclass

from src.app.exceptions import DomainValidationError


@dataclass(frozen=True)
class RuntimeResourceId:
    value: str

    def __post_init__(self) -> None:
        if isinstance(self.value, str) and self.value.strip():
            return
        raise DomainValidationError("invalid runtime resource id")
