from abc import abstractmethod
from typing import Protocol

from auth_service.application.auth.request_response_models import (
    Token,
    TokenPayload,
)


class JWTManageProtocol(Protocol):
    @abstractmethod
    def generate_token(self, sub: int) -> Token: ...

    @abstractmethod
    def parse_token(self, token: Token) -> TokenPayload | None: ...
