from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user.entity.model import User
from auth_service.domain.user.entity.fields import (
    Username,
    UserId,
)


class UserReadProtocol(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: Username) -> User | None: ...

    @abstractmethod
    async def get_all(self) -> list[User]: ...
