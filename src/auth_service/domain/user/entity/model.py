from dataclasses import dataclass

from auth_service.domain.user.entity.fields import (
    UserId,
    Username,
    UserHashedPassword,
)
from auth_service.domain.user.entity.enums import UserRoleEnum


@dataclass(frozen=True, kw_only=True)
class User:
    user_id: UserId
    username: Username
    role: UserRoleEnum
    password: UserHashedPassword | None
    is_active: bool
