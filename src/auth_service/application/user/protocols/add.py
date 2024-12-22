from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)


class UserCreateProtocol(Protocol):
    @abstractmethod
    async def create(
        self, username: Username, password: HashedPassword
    ) -> UserID | None: ...
