from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from auth_service.application.common.request_response_models import (
    SearchFilters,
)
from auth_service.application.user.request_response_models import (
    UserFullBodyResponse,
)
from auth_service.application.user.service import UserService
from auth_service.domain.user.enums import RoleEnum
from auth_service.presentation.common.schemes import PaginationParams

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/")
async def get_all(
    user_service: FromDishka[UserService],
    pagination: Annotated[PaginationParams, Depends()],
    filters: Annotated[SearchFilters, Depends()],
) -> list[UserFullBodyResponse]:
    return await user_service.get_all(
        pagination=pagination.to_model(),
        filters=filters,
    )


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    return await user_service.get_by_id(user_id=user_id)


@router.get("/username/{username}")
async def get_user_by_username(
    username: str, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    return await user_service.get_by_username(username=username)


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
