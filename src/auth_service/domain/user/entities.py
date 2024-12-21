from dataclasses import (
    dataclass,
)

from auth_service.domain.common.entities import (
    Entity,
)
from auth_service.domain.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)


@dataclass(
    slots=True,
    kw_only=True,
)
class User(Entity[UserID]):
    username: Username
    hashed_password: HashedPassword
