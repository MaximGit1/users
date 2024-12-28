from datetime import UTC, datetime

from jwt import (
    encode,
)

from auth_service.application.auth.protocols import JWTManageProtocol
from auth_service.application.auth.request_response_models import (
    Token,
    TokenPayload,
    TokenTypes,
)
from auth_service.main.config import jwt_settings


class AccessManagerRepository(JWTManageProtocol):
    def __init__(self):
        self._private_key = jwt_settings.private_key
        self._public_key = jwt_settings.public_key
        self._algorithm = jwt_settings.algorithm
        self._token_expire_minutes = jwt_settings.access_token_expire_minutes

    def generate_token(self, sub: int) -> Token:
        payload = self._generate_payload(sub=sub)
        return Token(encode(
            payload.to_dict(), self._private_key, algorithm=self._algorithm
        ))

    def parse_token(self, token: Token) -> TokenPayload | None:
        pass

    def _generate_payload(self, sub: int) -> TokenPayload:
        now = datetime.now(UTC).replace(tzinfo=None)
        expire = now + self._token_expire_minutes
        expire_as_int = int(expire.timestamp())

        return TokenPayload(
            sub=str(sub),
            expire=expire_as_int,
            token_type=TokenTypes.AccessToken,
        )
