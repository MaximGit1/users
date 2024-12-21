from enum import (
    StrEnum,
    auto,
)


class RoleEnum(StrEnum):
    GUEST = auto()
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()
