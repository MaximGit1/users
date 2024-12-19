from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: int | None
    username: str
    password: str | bytes | None
    role: str | None
    is_active: bool | None
