class UserApplicationError(Exception):
    pass


class UserAlreadyExistsError(UserApplicationError):
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists.")


class UserNotFoundError(UserApplicationError):
    def __init__(self, user_id: int = None, username: str = None):
        if user_id:
            super().__init__(f"User with ID '{user_id}' not found.")
        elif username:
            super().__init__(f"User with username '{username}' not found.")


# class InvalidPasswordError(UserApplicationError):
#     def __init__(self, reason: str):
#         super().__init__(f"Invalid password: {reason}")
#
#
# class InvalidRoleError(UserApplicationError):
#     def __init__(self, role: str):
#         super().__init__(f"Invalid role '{role}' for user.")

# class InvalidStatusChangeError(UserApplicationError):
#     def __init__(self, reason: str):
#         super().__init__(f"Invalid password: {reason}")
