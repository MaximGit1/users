from auth_service.domain.user.constraints.validations.constants import (
    USERNAME_MAX_LEN,
    USERNAME_MIN_LEN,
)
from auth_service.domain.user.constraints.validations.validators.base import (
    BaseValidator,
)


class UsernameValidator(BaseValidator):
    def __init__(self, username: str):
        self._username = username
        super().__init__()

    def validate_len_username(self) -> None:
        username_len = len(self._username)
        if username_len < USERNAME_MIN_LEN or username_len > USERNAME_MAX_LEN:
            raise self._throw_exception(
                f"The length of the username must be at least {USERNAME_MIN_LEN} and no more than {USERNAME_MAX_LEN}"
            )

    def validate_username_symbols(self) -> None:
        for char in self._username:
            if char not in self._symbols:
                raise self._throw_exception(
                    f"The username must contain allowed characters: `{self._symbols}` <== Not `{char}`"
                )

    def validate_username_start_char(self) -> None:
        username = self._username
        if not username[0].isalpha():
            raise self._throw_exception(
                f"The username ({username}) must start with a letter <== Not `{username[0]}`"
            )
