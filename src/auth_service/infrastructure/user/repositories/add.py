from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.application.user.protocols import UserCreateProtocol
from auth_service.domain.user.enums import RoleEnum
from auth_service.domain.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)
from auth_service.infrastructure.database.models import users_table


class UserCreateRepository(UserCreateProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self, username: Username, password: HashedPassword
    ) -> UserID | None:
        stmt = (
            users_table.insert()
            .values(
                {
                    "username": username.value,
                    "hashed_password": password.value,
                    "role": RoleEnum.USER,
                    "is_active": True,
                }
            )
            .returning(users_table.c.id)
        )

        try:
            result = await self._session.execute(stmt)
            new_id = result.scalar_one()
        except IntegrityError:
            return None

        return UserID(new_id)
