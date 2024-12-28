from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass(frozen=True)
class RoleInfo:
    name: str
    level: int


class RoleEnum(StrEnum):
    GUEST = auto()
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()

    @classmethod
    def get_roles(cls):
        return [RoleInfo(role, index) for index, role in enumerate(cls)]

    @classmethod
    def get_role_info(cls, role: "RoleEnum") -> RoleInfo:
        roles = {role: RoleInfo(role, index) for index, role in enumerate(cls)}
        return roles[role]

    @classmethod
    def validate_role(
        cls, user_role: "RoleEnum", required_role: "RoleEnum"
    ) -> bool:
        user_role_info = cls.get_role_info(user_role)
        required_role_info = cls.get_role_info(required_role)
        return user_role_info.level >= required_role_info.level
