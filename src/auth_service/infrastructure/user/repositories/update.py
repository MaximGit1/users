from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.application.user.protocols import UserUpdateProtocol
from auth_service.domain.user.enums import RoleEnum
from auth_service.domain.user.value_objects import UserID
from auth_service.infrastructure.database.models import users_table


class UserUpdateRepository(UserUpdateProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def change_status(self, user_id: UserID, *, is_active: bool) -> None:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(is_active=is_active)
        )

        await self._session.execute(stmt)

    async def change_role(self, user_id: UserID, role: RoleEnum) -> None:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(role=role)
        )

        await self._session.execute(stmt)
