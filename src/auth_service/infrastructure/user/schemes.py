from pydantic import BaseModel

from auth_service.domain.user.value_objects import RawPassword, Username


class UserCreateScheme(BaseModel):
    username: str
    password: str

    def get_data(self):
        return Username(self.username), RawPassword(self.password)
