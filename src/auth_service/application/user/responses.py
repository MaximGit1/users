from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class UserIdResponse:
    user_id: int
