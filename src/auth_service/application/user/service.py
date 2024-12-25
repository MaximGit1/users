from auth_service.application.common.protocols import UoWProtocol
from auth_service.application.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth_service.application.user.protocols import (
    PasswordHasherProtocol,
    UserCreateProtocol,
    UserReadProtocol,
    UserUpdateProtocol,
)
from auth_service.application.user.responses import (
    UserFullBodyResponse,
    UserIdResponse,
)
from auth_service.domain.user.enums import RoleEnum
from auth_service.domain.user.value_objects import (
    RawPassword,
    UserID,
    Username,
)


class UserService:
    def __init__(
        self,
        add_repository: UserCreateProtocol,
        read_repository: UserReadProtocol,
        update_repository: UserUpdateProtocol,
        password_hasher: PasswordHasherProtocol,
        uow: UoWProtocol,
    ) -> None:
        self._password_hasher = password_hasher
        self._add = add_repository
        self._read = read_repository
        self._update = update_repository
        self._uow = uow

    async def create_user(
        self, username: Username, password: RawPassword
    ) -> UserIdResponse:
        hashed_password = self._password_hasher.hash_password(
            password=password
        )
        user_id = await self._add.create(
            username=username, password=hashed_password
        )

        if user_id is None:
            await self._uow.rollback()
            raise UserAlreadyExistsError(username=username.value)

        await self._uow.commit()
        return UserIdResponse(user_id=user_id.value)

    async def get_by_id(self, user_id: int) -> UserFullBodyResponse:
        user = await self._read.get_by_id(user_id=UserID(user_id))

        if user is None:
            raise UserNotFoundError(user_id=user_id)

        return UserFullBodyResponse(
            user_id=user.id.value,
            username=user.username.value,
            role=user.role,
            is_active=user.is_active,
        )

    async def get_by_username(self, username: str) -> UserFullBodyResponse:
        user = await self._read.get_by_username(username=Username(username))

        if user is None:
            raise UserNotFoundError(username=username)

        return UserFullBodyResponse(
            user_id=user.id.value,
            username=user.username.value,
            role=user.role,
            is_active=user.is_active,
        )

    async def get_all(
        self, offset: int = 0, limit: int = 10
    ) -> list[UserFullBodyResponse]:
        users_list = await self._read.get_all(
            offset=offset,
            limit=limit,
        )

        return [
            UserFullBodyResponse(
                user_id=user.id.value,
                username=user.username.value,
                role=user.role,
                is_active=user.is_active,
            )
            for user in users_list
        ]

    async def change_role(self, user_id: int, role: RoleEnum) -> None:
        await self._update.change_role(
            user_id=UserID(user_id),
            role=role,
        )
        await self._uow.commit()

    async def change_status(self, user_id: int, *, is_active: bool) -> None:
        await self._update.change_status(
            user_id=UserID(user_id), is_active=is_active
        )
        await self._uow.commit()
