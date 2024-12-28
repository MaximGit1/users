from auth_service.application.auth.exceptions import InvalidTokenTypeError
from auth_service.application.auth.protocols import JWTManageProtocol
from auth_service.application.auth.request_response_models import (
    Token,
    TokenTypes,
)


class AuthService:
    def __init__(
        self,
        access_token_repository: JWTManageProtocol,
    ):
        self._access = access_token_repository

    def login_user(self, user_id: int) -> Token:
        return self._generate_access_token(sub=user_id)

    def _generate_access_token(self, sub: int) -> Token:
        return self._generate_token(
            sub=sub,
            token_type=TokenTypes.AccessToken,
        )

    def _generate_token(self, sub: int, token_type: TokenTypes) -> Token:
        if token_type == TokenTypes.AccessToken:
            return self._access.generate_token(sub=sub)
        elif token_type == TokenTypes.RefreshToken:
            raise InvalidTokenTypeError(token_type=token_type)
        else:
            raise InvalidTokenTypeError(token_type=token_type)
