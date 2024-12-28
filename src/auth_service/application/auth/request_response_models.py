from dataclasses import dataclass
from enum import StrEnum
from typing import NewType

Token = NewType("Token", str)


class TokenTypes(StrEnum):
    AccessToken = "access"
    RefreshToken = "refresh"


@dataclass
class TokenPayload:
    sub: str
    expire: int
    token_type: TokenTypes

    def to_dict(self) -> dict:
        return {
            "sub": self.sub,
            "expire": self.expire,
            "token_type": self.token_type,
        }
