class DomainError(Exception):
    """Base class for exceptions in this module."""


class DomainValidationError(DomainError):
    """Exception for domain validation errors"""
