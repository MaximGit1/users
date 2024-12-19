from bcrypt import gensalt, hashpw, checkpw

from auth_service.domain.salt.protocols import SaltProtocol
from auth_service.domain.user import UserRawPassword, UserHashedPassword
from auth_service.domain.user.entity.fields import UserHashedPassword


class SaltRepository(SaltProtocol):
    def hash_password(self, password: UserRawPassword) -> UserHashedPassword:
        hashed_password = hashpw(
            password=password.value.encode(),
            salt=gensalt(),
        )
        return UserHashedPassword(hashed_password)

    def validate_password(
        self, password: UserRawPassword, hashed_password: UserHashedPassword
    ) -> bool:
        return checkpw(
            password=password.value.encode(),
            hashed_password=hashed_password.value,
        )
