from auth_service.application.common.exceptions import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists.")
