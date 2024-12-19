from collections.abc import AsyncIterator
from typing import NewType
import os

from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth_service.domain.uow.protocols import UoWProtocol
from auth_service.domain.user.protocols import (
    UserCreateProtocol,
    UserReadProtocol,
    UserUpdateProtocol,
)
from auth_service.domain.salt.protocols import SaltProtocol

from auth_service.infrastructure.repositories.user_repository import (
    UserCreateRepository,
    UserReadRepository,
    UserUpdateRepository,
)
from auth_service.infrastructure.repositories.salt_repository import (
    SaltRepository,
)

from auth_service.application.user.service import UserService


DBURI = NewType("DBURI", str)


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def db_uri(self) -> DBURI:
        db_uri = os.getenv("DB_URI")
        if db_uri is None:
            raise ValueError("DB_URI is not set")
        return DBURI(db_uri)

    @provide(scope=Scope.APP)
    async def create_engine(self, db_uri: DBURI) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            db_uri,
            echo=True,
            # pool_size=15,
            # max_overflow=15,
            # connect_args={"connect_timeout": 5},
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def create_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def new_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AnyOf[AsyncSession, UoWProtocol]]:
        async with session_factory() as session:
            yield session


def repository_provider() -> Provider:
    provider = Provider()
    provider.provide(
        UserCreateRepository,
        scope=Scope.REQUEST,
        provides=UserCreateProtocol,
    )
    provider.provide(
        SaltRepository,
        scope=Scope.APP,
        provides=SaltProtocol,
    )
    provider.provide(
        UserReadRepository,
        scope=Scope.REQUEST,
        provides=UserReadProtocol,
    )
    provider.provide(
        UserUpdateRepository,
        scope=Scope.REQUEST,
        provides=UserUpdateProtocol,
    )

    return provider


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(UserService, scope=Scope.REQUEST)

    return provider


def init_async_container() -> AsyncContainer:
    providers = [
        DBProvider(),
        repository_provider(),
        service_provider(),
    ]

    return make_async_container(*providers)
