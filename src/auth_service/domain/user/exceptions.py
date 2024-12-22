from auth_service.domain.common.exceptions import DomainError


class UserDomainValidationError(DomainError):
    """Exception for domain validation errors"""
