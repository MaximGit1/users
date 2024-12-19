from abc import ABC

from auth_service.domain.user.constraints.validations.constants import (
    ALLOWED_CHARS,
)
from auth_service.domain.user.constraints.exceptions import (
    UserDomainFieldError,
)


class BaseValidator(ABC):
    def __init__(self):
        self._symbols = ALLOWED_CHARS
        self._load_validators()

    def _load_validators(self) -> None:
        for method_name in dir(self):
            if method_name.startswith("validate") and callable(
                getattr(self, method_name)
            ):
                getattr(self, method_name)()

    def _throw_exception(self, message: str):
        raise UserDomainFieldError(message)
