from abc import abstractmethod
from typing import Protocol

from auth_service.domain.user import UserRawPassword, UserHashedPassword


class SaltProtocol(Protocol):
    @abstractmethod
    def hash_password(
        self, password: UserRawPassword
    ) -> UserHashedPassword: ...

    @abstractmethod
    def validate_password(
        self, password: UserRawPassword, hashed_password: UserHashedPassword
    ) -> bool: ...
