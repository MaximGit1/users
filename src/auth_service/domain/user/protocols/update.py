from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user.entity.fields import UserId
from auth_service.domain.user.entity.enums import UserRoleEnum


class UserUpdateProtocol(Protocol):
    @abstractmethod
    async def change_status(self, user_id: UserId, status: bool) -> bool: ...

    @abstractmethod
    async def change_role(
        self, user_id: UserId, role: UserRoleEnum
    ) -> bool: ...
