from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from auth_service.application.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth_service.application.user.responses import (
    UserIdResponse,
    UserFullBodyResponse,
)
from auth_service.domain.user import UserId, Username, UserRoleEnum
from auth_service.domain.user.constraints.exceptions import (
    UserDomainFieldError,
)
from auth_service.infrastructure.schemes.user import UserCreateScheme
from auth_service.application.user.service import UserService
from auth_service.presentation.user_exceptions import (
    UserAlreadyExistsError409,
    UserFieldError409,
    UserNoFoundError404,
)
from underLogs import get_logger

logger = get_logger("my_json_logger")
router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.post("/create/", status_code=201)
async def create_user(
    user_data: UserCreateScheme, user_service: FromDishka[UserService]
) -> UserIdResponse:
    try:
        username, password = user_data.to_model()
    except UserDomainFieldError as e:
        logger.info(e, exc_info=True)
        raise UserFieldError409

    try:
        user_id = await user_service.create_user(
            username=username, password=password
        )
        return user_id
    except UserAlreadyExistsError:
        raise UserAlreadyExistsError409


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    try:
        user = await user_service.get_by_id(user_id=UserId(user_id))
        return user
    except UserNotFoundError:
        raise UserNoFoundError404


@router.get("/username/{username}")
async def get_user_by_username(
    username: str, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    try:
        user = await user_service.get_by_username(username=Username(username))
        return user
    except UserNotFoundError:
        raise UserNoFoundError404


@router.get("/")
async def get_all_users(
    user_service: FromDishka[UserService],
) -> list[UserFullBodyResponse]:
    return await user_service.get_all()


@router.patch("/{user_id}/update/status")
async def update_user_status(
    user_id: int, is_active: bool, user_service: FromDishka[UserService]
) -> None:
    try:
        if is_active:
            await user_service.activate_user_status(user_id=UserId(user_id))
        else:
            await user_service.deactivate_user_status(user_id=UserId(user_id))
    except UserNotFoundError:
        raise UserNoFoundError404


@router.patch("/{user_id}/update/role")
async def update_user_role(
    user_id: int, role: UserRoleEnum, user_service: FromDishka[UserService]
) -> None:
    try:
        await user_service.change_role(user_id=UserId(user_id), new_role=role)
    except UserNotFoundError:
        raise UserNoFoundError404
