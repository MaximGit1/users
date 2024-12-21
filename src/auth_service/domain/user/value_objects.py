from dataclasses import dataclass

from auth_service.domain.common.exceptions import DomainValidationError
from auth_service.domain.common.value_objects import ValueObject
from .constants import (
    PASSWORD_MAX_LEN,
    PASSWORD_MIN_LEN,
    USERNAME_MAX_LEN,
    USERNAME_MIN_LEN,
)


@dataclass(frozen=True)
class UserID(ValueObject, int):
    pass


@dataclass(frozen=True)
class Username(ValueObject[str]):
    def validate(self) -> None:
        username_len = len(self._value)

        if username_len < USERNAME_MIN_LEN:
            raise DomainValidationError(
                f"Username must be more than "
                f"{USERNAME_MIN_LEN} characters"
            )

        if username_len > USERNAME_MAX_LEN:
            raise DomainValidationError(
                f"Username must be less than "
                f"{USERNAME_MAX_LEN} characters"
            )


@dataclass(frozen=True)
class RawPassword(ValueObject[str]):
    def validate(self) -> None:
        password_len = len(self._value)

        if password_len < PASSWORD_MIN_LEN:
            raise DomainValidationError(
                f"User password must be more than "
                f"{PASSWORD_MIN_LEN} characters"
            )

        if password_len > PASSWORD_MAX_LEN:
            raise DomainValidationError(
                f"User password must be less than "
                f"{USERNAME_MAX_LEN} characters"
            )


@dataclass(frozen=True)
class HashedPassword(ValueObject[bytes]):
    pass
