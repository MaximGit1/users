from auth_service.application.common.protocols import UoWProtocol
from auth_service.application.user.exceptions import UserAlreadyExistsError
from auth_service.application.user.protocols import (
    PasswordHasherProtocol,
    UserCreateProtocol,
)
from auth_service.application.user.responses import (
    UserIdResponse,
)
from auth_service.domain.user.value_objects import (
    RawPassword,
    Username,
)


class UserService:
    def __init__(
        self,
        add_repository: UserCreateProtocol,
        password_hasher: PasswordHasherProtocol,
        uow: UoWProtocol,
    ) -> None:
        self._password_hasher = password_hasher
        self._add = add_repository
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
