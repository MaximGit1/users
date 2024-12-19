from auth_service.domain.user.constraints.validations.constants import (
    USER_PASSWORD_MIN_LEN,
    USER_PASSWORD_MAX_LEN,
)
from auth_service.domain.user.constraints.validations.validators.base import (
    BaseValidator,
)


class UserPasswordValidator(BaseValidator):
    def __init__(self, password: str):
        self._password = password
        super().__init__()

    def validate_len_password(self) -> None:
        password_len = len(self._password)
        if (
            password_len < USER_PASSWORD_MIN_LEN
            or password_len > USER_PASSWORD_MAX_LEN
        ):
            raise self._throw_exception(
                f"The length of the password must be at least {USER_PASSWORD_MIN_LEN} and no more than {USER_PASSWORD_MAX_LEN}"
            )

    def validate_password_symbols(self) -> None:
        for char in self._password:
            if char not in self._symbols:
                raise self._throw_exception(
                    f"The password must contain allowed characters: `{self._symbols}` <== Not `{char}`"
                )

    def validate_password_start_char(self) -> None:
        password = self._password
        if not password[0].isalpha():
            raise self._throw_exception(
                f"The password ({password}) must start with a letter <== Not `{password[0]}`"
            )
