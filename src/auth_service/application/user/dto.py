from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: int
    username: str
    password: bytes | None
    role: str
    is_active: bool
