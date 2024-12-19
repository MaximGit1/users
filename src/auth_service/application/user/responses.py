from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class UserIdResponse:
    user_id: int


@dataclass(frozen=True, kw_only=True)
class UserFullBodyResponse:
    user_id: int
    username: str
    role: str
    is_active: bool


# @dataclass(frozen=True, kw_only=True)
# class UserUpdatedResponse:
#     is_updated: bool
