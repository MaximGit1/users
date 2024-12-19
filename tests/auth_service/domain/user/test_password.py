import pytest

from auth_service.domain.user.constraints.exceptions import (
    UserDomainFieldError,
)
from auth_service.domain.user.entity.fields import UserRawPassword
from auth_service.domain.user.constraints.validations.constants import (
    USER_PASSWORD_MAX_LEN,
    USER_PASSWORD_MIN_LEN,
)

VALID_PASSWORD = "ValidPassword123!"
INVALID_PASSWORD_TOO_SHORT = "A1!"
INVALID_PASSWORD_TOO_LONG = "A" * (USER_PASSWORD_MAX_LEN + 1) + "1!"
INVALID_PASSWORD_SYMBOLS = "Password@#"
INVALID_PASSWORD_STARTS_WITH_NUMBER = "1ValidPassword!"


def test_valid_password():
    password = UserRawPassword(VALID_PASSWORD)
    assert password.value == VALID_PASSWORD


def test_password_too_short():
    with pytest.raises(
        UserDomainFieldError,
        match=f"The length of the password must be at least {USER_PASSWORD_MIN_LEN}",
    ):
        UserRawPassword(INVALID_PASSWORD_TOO_SHORT)


def test_password_too_long():
    with pytest.raises(
        UserDomainFieldError,
        match=f"The length of the password must be at least {USER_PASSWORD_MIN_LEN}",
    ):
        UserRawPassword(INVALID_PASSWORD_TOO_LONG)


def test_password_invalid_symbols():
    with pytest.raises(
        UserDomainFieldError,
        match="The password must contain allowed characters",
    ):
        UserRawPassword(INVALID_PASSWORD_SYMBOLS)


def test_password_start_with_letter():
    with pytest.raises(
        UserDomainFieldError,
        match="The password .* must start with a letter",
    ):
        UserRawPassword(INVALID_PASSWORD_STARTS_WITH_NUMBER)


@pytest.mark.parametrize(
    "password",
    [
        "ValidPassword123!",
        "AnotherOne42$",
        "Zuper$trongP_ssword1",
    ],
)
def test_valid_password_cases(password):
    user_password = UserRawPassword(password)
    assert user_password.value == password
