from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from auth_service.application.user.responses import (
    UserFullBodyResponse,
    UserIdResponse,
)
from auth_service.application.user.service import UserService
from auth_service.domain.user.enums import RoleEnum
from auth_service.infrastructure.user.schemes import UserCreateScheme

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/")
async def get_all(
    user_service: FromDishka[UserService],
) -> list[UserFullBodyResponse]:
    return await user_service.get_all()


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    return await user_service.get_by_id(user_id=user_id)


@router.get("/username/{username}")
async def get_user_by_username(
    username: str, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    if username == "raise":
        raise IndexError("raise")
    return await user_service.get_by_username(username=username)


@router.post("/create/", status_code=201)
async def create_user(
    user_data: UserCreateScheme, user_service: FromDishka[UserService]
) -> UserIdResponse:
    username, password = user_data.get_data()

    return await user_service.create_user(username=username, password=password)


@router.patch("/{user_id}/update/role")
async def update_role(
    user_id: int,
    role: RoleEnum,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.change_role(
        user_id=user_id,
        role=role,
    )


@router.patch("/{user_id}/update/status/")
async def update_user_status(
    user_id: int,
    *,
    is_active: bool,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.change_status(
        user_id=user_id,
        is_active=is_active,
    )
