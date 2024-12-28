from auth_service.application.common.exceptions import ApplicationError


class InvalidTokenTypeError(ApplicationError):
    def __init__(self, token_type: str):
        super().__init__(f"Invalid token type='{token_type}'.")


class TokenExpiredError(ApplicationError):
    def __init__(self):
        super().__init__("Token expired.")
