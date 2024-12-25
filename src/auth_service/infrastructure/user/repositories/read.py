from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.application.user.protocols import UserReadProtocol
from auth_service.domain.user.entities import User
from auth_service.domain.user.enums import RoleEnum
from auth_service.domain.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)
from auth_service.infrastructure.database.models import users_table


class UserReadRepository(UserReadProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UserID) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id.value)
        result = (await self._session.execute(stmt)).one_or_none()

        if result is None:
            return None

        return self._load_user(result)

    async def get_by_username(self, username: Username) -> User | None:
        stmt = select(users_table).where(
            users_table.c.username == username.value
        )
        result = (await self._session.execute(stmt)).one_or_none()

        if result is None:
            return None

        return self._load_user(result)

    async def get_all(self) -> list[User]:
        stmt = select(users_table)
        result = await self._session.execute(stmt)

        return self._load_users(result.all())

    def _load_user(self, row: Row[Any]) -> User:
        return User(
            id=UserID(row.id),
            username=Username(row.username),
            hashed_password=HashedPassword(row.hashed_password),
            role=self._convert_role(row.role),
            is_active=row.is_active,
        )

    @staticmethod
    def _convert_role(role: str) -> RoleEnum:
        if role == RoleEnum.USER:
            return RoleEnum.USER
        elif role == RoleEnum.ADMIN:
            return RoleEnum.ADMIN
        elif role == RoleEnum.MODERATOR:
            return RoleEnum.MODERATOR
        else:
            return RoleEnum.GUEST

    def _load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self._load_user(row) for row in rows]
