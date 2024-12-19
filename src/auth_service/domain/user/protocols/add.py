from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user.entity.fields import (
    Username,
    UserHashedPassword,
    UserId,
)


class UserCreateProtocol(Protocol):
    @abstractmethod
    async def create(
        self, username: Username, password: UserHashedPassword
    ) -> UserId | None: ...
