from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from auth_service.application.auth.request_response_models import Token
from auth_service.application.auth.service import AuthService
from auth_service.application.user.request_response_models import (
    UserIdResponse,
)
from auth_service.application.user.service import UserService
from auth_service.domain.user.enums import RoleEnum
from auth_service.presentation.auth.schemes import UserLoginInput
from auth_service.presentation.user.schemes import UserCreateScheme

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/register/", status_code=201)
async def create_user(
    user_data: Annotated[UserCreateScheme, Depends()],
    user_service: FromDishka[UserService],
) -> UserIdResponse:
    username, password = user_data.get_data()

    return await user_service.create_user(username=username, password=password)


@router.post("/login/")
async def login(
    user_data: Annotated[UserLoginInput, Depends()],
    user_service: FromDishka[UserService],
    auth_service: FromDishka[AuthService],
) -> Token:
    username, password = user_data.get_data()
    user_id = await user_service.authenticate_user(
        username=username, password=password
    )
    return auth_service.login_user(user_id=user_id)


@router.post("/verify-role/")
async def verify_role(
    user_id: int,
    role: RoleEnum,
    user_service: FromDishka[UserService],
) -> bool:
    return await user_service.verify_role(
        user_id=user_id,
        required_role=role,
    )
