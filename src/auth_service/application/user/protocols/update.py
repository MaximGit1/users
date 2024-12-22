from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user.enums import RoleEnum
from auth_service.domain.user.value_objects import UserID


class UserUpdateProtocol(Protocol):
    @abstractmethod
    async def change_status(
        self, user_id: UserID, *, status: bool
    ) -> bool: ...

    @abstractmethod
    async def change_role(self, user_id: UserID, role: RoleEnum) -> bool: ...
