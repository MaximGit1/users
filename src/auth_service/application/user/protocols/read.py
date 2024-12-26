from abc import abstractmethod
from typing import Protocol

from auth_service.application.user.request import (
    PaginationParams,
    SearchFilters,
)
from auth_service.domain.user.entities import User
from auth_service.domain.user.value_objects import (
    UserID,
    Username,
)


class UserReadProtocol(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: Username) -> User | None: ...

    @abstractmethod
    async def get_all(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[User]: ...
