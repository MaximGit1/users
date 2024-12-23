from auth_service.application.common.exceptions import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists.")


class UserNotFoundError(ApplicationError):
    def __init__(
        self, user_id: int | None = None, username: str | None = None
    ):
        msg = "User with "

        if user_id:
            msg += f"id={user_id} "
        if username:
            msg += f"username={username} "

        msg += "not found."

        super().__init__(msg)
