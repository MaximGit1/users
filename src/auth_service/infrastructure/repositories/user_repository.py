from typing import Any, Sequence

from sqlalchemy import Row, select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from auth_service.domain.user import (
    Username,
    UserHashedPassword,
    UserId,
    UserRoleEnum,
    User,
)
from auth_service.domain.user.protocols import (
    UserCreateProtocol,
    UserReadProtocol,
    UserUpdateProtocol,
)
from auth_service.infrastructure.database.models import users_table
from auth_service.application.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth_service.application.user.dto import UserDTO
from underLogs import get_logger


logger = get_logger("my_json_logger")


class UserCreateRepository(UserCreateProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self, username: Username, password: UserHashedPassword
    ) -> UserId | None:
        stmt = (
            users_table.insert()
            .values(
                {
                    "username": username.value,
                    "hashed_password": password.value,
                    "role": UserRoleEnum.USER,
                    "is_active": True,
                }
            )
            .returning(users_table.c.id)
        )
        try:
            result = await self._session.execute(stmt)
            new_id = result.scalar_one()
            return UserId(new_id)
        except IntegrityError as e:
            logger.exception(e, exc_info=True)
            raise UserAlreadyExistsError(username=username.value)


class UserReadRepository(UserReadProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UserId) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id.value)
        result = (await self._session.execute(stmt)).one_or_none()
        if result is None:
            raise UserNotFoundError(user_id=user_id.value)
        return self._load_user(result)

    async def get_by_username(self, username: Username) -> User | None:
        stmt = select(users_table).where(
            users_table.c.username == username.value
        )
        result = (await self._session.execute(stmt)).one_or_none()
        if result is None:
            raise UserNotFoundError(username=username.value)
        return self._load_user(result)

    async def get_all(self) -> list[User]:
        stmt = select(users_table)
        result = await self._session.execute(stmt)
        return self._load_users(result.all())

    def _load_user(self, row: Row[Any]) -> User:
        dto = UserDTO(
            user_id=row.id,
            username=row.username,
            password=row.hashed_password,
            role=row.role,
            is_active=row.is_active,
        )
        return User(
            user_id=UserId(dto.user_id),
            username=Username(dto.username),
            password=None,
            role=self._convert_role(dto.role),
            is_active=dto.is_active,
        )

    def _load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self._load_user(row) for row in rows]

    @staticmethod
    def _convert_role(role: str) -> UserRoleEnum:
        if role == UserRoleEnum.USER:
            return UserRoleEnum.USER
        elif role == UserRoleEnum.ADMIN:
            return UserRoleEnum.ADMIN
        else:
            return UserRoleEnum.GUEST


class UserUpdateRepository(UserUpdateProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def change_status(self, user_id: UserId, status: bool) -> bool:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(is_active=status)
        )
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            return False

        return True

    async def change_role(self, user_id: UserId, role: UserRoleEnum) -> bool:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(role=role)
        )
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            return False

        return True
