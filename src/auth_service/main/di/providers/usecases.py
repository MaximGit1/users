from dishka import (
    Provider,
    Scope,
)

from auth_service.application.user.service import UserService


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(UserService, scope=Scope.REQUEST)

    return provider


def get_use_cases_providers() -> list[Provider]:
    return [
        service_provider(),
    ]
