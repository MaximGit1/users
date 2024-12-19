import pytest

from auth_service.domain.user import (
    User,
    UserId,
    Username,
    UserRawPassword,
    UserHashedPassword,
    UserRoleEnum,
)
from auth_service.domain.user.constraints.validations.constants import (
    USERNAME_MIN_LEN,
    USERNAME_MAX_LEN,
)
from auth_service.domain.user.constraints.exceptions import (
    UserDomainFieldError,
)

TEST_USER_ID = UserId(1)
TEST_PASSWORD = UserRawPassword("TestPassword231!")
TEST_ROLE = UserRoleEnum.USER
TEST_IS_ACTIVE = True
TEST_NAME = "ValidName_" * 5


@pytest.fixture
def create_user():
    def _create_user(
        user_id=TEST_USER_ID,
        username=Username("ValidName_"),
        role=TEST_ROLE,
        password=TEST_PASSWORD,
        is_active=TEST_IS_ACTIVE,
    ):
        hashed_password = UserHashedPassword(password.value.encode())
        return User(
            user_id=user_id,
            username=username,
            role=role,
            password=hashed_password,
            is_active=is_active,
        )

    return _create_user


def test_username_normal_len(create_user):
    diff = USERNAME_MAX_LEN - USERNAME_MIN_LEN
    normal_len = USERNAME_MIN_LEN + diff // 2
    username = TEST_NAME[:normal_len]
    user = create_user(username=Username(username))
    assert user.username.value == username


def test_little_name_len(create_user):
    username = TEST_NAME[: USERNAME_MIN_LEN - 1]
    with pytest.raises(
        UserDomainFieldError,
        match="The length of the username must be at least",
    ):
        create_user(username=Username(username))


@pytest.mark.parametrize(
    "username",
    [
        TEST_NAME[:USERNAME_MIN_LEN],
        TEST_NAME[:USERNAME_MAX_LEN],
    ],
)
def test_username_edge_lengths(create_user, username):
    user = create_user(username=Username(username))
    assert user.username.value == username


def test_username_too_long(create_user):
    username = TEST_NAME[: USERNAME_MAX_LEN + 1]
    with pytest.raises(
        UserDomainFieldError,
        match="The length of the username must be at least",
    ):
        create_user(username=Username(username))
