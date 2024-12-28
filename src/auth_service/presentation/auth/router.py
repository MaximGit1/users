from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from auth_service.application.auth.request_response_models import Token
from auth_service.application.auth.service import AuthService
from auth_service.application.user.service import UserService
from auth_service.presentation.auth.schemes import UserLoginInput

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


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
