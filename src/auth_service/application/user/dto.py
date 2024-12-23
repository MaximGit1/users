from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: int
    username: str
    password: bytes
    role: str
    is_active: bool
