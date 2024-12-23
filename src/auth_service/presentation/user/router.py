from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from auth_service.application.user.responses import UserIdResponse
from auth_service.application.user.service import UserService
from auth_service.infrastructure.user.schemes import UserCreateScheme

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.post("/create/", status_code=201)
async def create_user(
    user_data: UserCreateScheme, user_service: FromDishka[UserService]
) -> UserIdResponse:
    username, password = user_data.get_data()

    return await user_service.create_user(username=username, password=password)
