from auth_service.domain.user.entity.model import User
from auth_service.domain.user.entity.fields import (
    UserId,
    Username,
    UserRawPassword,
)
from auth_service.domain.user.entity.enums import UserRoleEnum
from auth_service.domain.user.protocols import (
    UserCreateProtocol,
    UserUpdateProtocol,
    UserReadProtocol,
)

from auth_service.domain.uow.protocols import UoWProtocol
from auth_service.domain.salt.protocols import SaltProtocol

from auth_service.application.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)

from auth_service.application.user.responses import (
    UserIdResponse,
    UserFullBodyResponse,
)
from underLogs import get_logger
from auth_service.application.user.exceptions import UserAlreadyExistsError

logger = get_logger("my_json_logger")


class UserService:
    def __init__(
        self,
        read: UserReadProtocol,
        create: UserCreateProtocol,
        update: UserUpdateProtocol,
        salt: SaltProtocol,
        uow: UoWProtocol,
    ):
        self._user_read = read
        self._user_add = create
        self._user_update = update
        self._salt = salt
        self._uow = uow

    async def create_user(
        self, username: Username, password: UserRawPassword
    ) -> UserIdResponse | None:
        hashed_password = self._salt.hash_password(password=password)
        try:
            user_id = await self._user_add.create(
                username=username, password=hashed_password
            )
            await self._uow.commit()
            return UserIdResponse(user_id=user_id.value)
        except UserAlreadyExistsError as e:
            logger.exception(e, exc_info=True)
            await self._uow.rollback()
            raise UserAlreadyExistsError(username=username.value)

    async def get_all(self) -> list[UserFullBodyResponse]:
        users_list = await self._user_read.get_all()
        users_response_list: list[UserFullBodyResponse] = []
        for index in range(0, len(users_list)):
            users_response_list.append(
                UserFullBodyResponse(
                    user_id=users_list[index].user_id.value,
                    username=users_list[index].username.value,
                    role=users_list[index].role,
                    is_active=users_list[index].is_active,
                )
            )
        return users_response_list

    async def get_by_id(self, user_id: UserId) -> UserFullBodyResponse | None:
        user = await self._user_read.get_by_id(user_id=user_id)

        if user is None:
            raise UserNotFoundError(user_id=user_id.value)

        return UserFullBodyResponse(
            user_id=user.user_id.value,
            username=user.username.value,
            role=user.role,
            is_active=user.is_active,
        )

    async def get_by_username(
        self, username: Username
    ) -> UserFullBodyResponse | None:
        user = await self._user_read.get_by_username(username=username)

        if user is None:
            raise UserNotFoundError(username=username.value)

        return UserFullBodyResponse(
            user_id=user.user_id.value,
            username=user.username.value,
            role=user.role,
            is_active=user.is_active,
        )

    async def activate_user_status(self, user_id: UserId) -> bool:
        is_updated = await self._user_update.change_status(
            user_id=user_id, status=True
        )
        if is_updated:
            await self._uow.commit()
        else:
            await self._uow.rollback()
            raise UserNotFoundError(user_id=user_id.value)

    async def deactivate_user_status(self, user_id: UserId) -> None:
        is_updated = await self._user_update.change_status(
            user_id=user_id, status=False
        )
        if is_updated:
            await self._uow.commit()
        else:
            await self._uow.rollback()
            raise UserNotFoundError(user_id=user_id.value)

    async def change_role(
        self, user_id: UserId, new_role: UserRoleEnum
    ) -> None:
        is_updated = await self._user_update.change_role(
            user_id=user_id, role=new_role
        )
        if is_updated:
            await self._uow.commit()
        else:
            await self._uow.rollback()
            raise UserNotFoundError(user_id=user_id.value)
