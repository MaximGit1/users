from pydantic import BaseModel

from auth_service.domain.user import UserRawPassword, Username


class UserCreateScheme(BaseModel):
    username: str
    password: str

    def to_model(self):
        return Username(self.username), UserRawPassword(self.password)
