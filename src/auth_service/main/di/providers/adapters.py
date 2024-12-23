import os
from collections.abc import AsyncIterator
from typing import NewType

from dishka import (
    AnyOf,
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth_service.application.common.protocols.uow import UoWProtocol
from auth_service.application.user.protocols import (
    PasswordHasherProtocol,
    UserCreateProtocol,
    UserReadProtocol,
)
from auth_service.infrastructure.user.repositories import (
    PasswordHasherRepository,
    UserCreateRepository,
    UserReadRepository,
)

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
        PasswordHasherRepository,
        scope=Scope.APP,
        provides=PasswordHasherProtocol,
    )
    provider.provide(
        UserReadRepository,
        scope=Scope.REQUEST,
        provides=UserReadProtocol,
    )

    return provider


def get_adapters_providers() -> list[Provider]:
    return [
        DBProvider(),
        repository_provider(),
    ]
