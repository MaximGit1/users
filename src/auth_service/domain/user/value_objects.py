from dataclasses import dataclass

from auth_service.domain.common.value_objects import ValueObject
from auth_service.domain.user.exceptions import UserDomainValidationError


@dataclass(frozen=True)
class UserID(ValueObject, int):
    pass


@dataclass(frozen=True)
class Username(ValueObject[str]):
    def validate(self) -> None:
        username_min_len = 4
        username_max_len = 15

        username_len = len(self.value)

        if username_len < username_min_len:
            raise UserDomainValidationError(
                f"Username must be more than " f"{username_min_len} characters"
            )

        if username_len > username_max_len:
            raise UserDomainValidationError(
                f"Username must be less than " f"{username_max_len} characters"
            )


@dataclass(frozen=True)
class RawPassword(ValueObject[str]):
    def validate(self) -> None:
        password_min_len = 8
        password_max_len = 32

        password_len = len(self.value)

        if password_len < password_min_len:
            raise UserDomainValidationError(
                f"User password must be more than "
                f"{password_min_len} characters"
            )

        if password_len > password_max_len:
            raise UserDomainValidationError(
                f"User password must be less than "
                f"{password_max_len} characters"
            )


@dataclass(frozen=True)
class HashedPassword(ValueObject[bytes]):
    pass
