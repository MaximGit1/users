from dishka import AsyncContainer, make_async_container

from auth_service.main.di.providers.adapters import get_adapters_providers
from auth_service.main.di.providers.usecases import get_use_cases_providers


def container_factory() -> AsyncContainer:
    return make_async_container(
        *get_adapters_providers(),
        *get_use_cases_providers(),
    )
