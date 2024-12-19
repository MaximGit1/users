from dataclasses import dataclass

from auth_service.domain.user.constraints.validations.validators import (
    UsernameValidator,
    UserPasswordValidator,
)


@dataclass(frozen=True)
class UserId:
    value: int


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        UsernameValidator(self.value)


@dataclass(frozen=True)
class UserHashedPassword:
    value: bytes


@dataclass(frozen=True)
class UserRawPassword:
    value: str

    def __post_init__(self) -> None:
        UserPasswordValidator(self.value)
