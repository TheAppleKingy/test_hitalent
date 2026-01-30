from typing import AsyncGenerator

from dishka import make_async_container, Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
    AsyncSession
)

from src.application.interfaces.repositories import *
from src.application.interfaces import *
from src.application.use_cases import *
from src.infra.configs import DBConfig
from src.infra.repositories import *
from src.infra.uow import AlchemyUoW


class DBProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_conf(self) -> DBConfig:
        return DBConfig()  # type: ignore

    @provide
    def get_engine(self, config: DBConfig) -> AsyncEngine:
        return create_async_engine(config.conn_url)

    @provide
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=True,
            autobegin=False
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            try:
                yield session
            finally:
                await session.close()

    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UoWInterface:
        return AlchemyUoW(session)


repo_provider = Provider(scope=Scope.REQUEST)
repo_provider.provide(AlchemyChatRepository, provides=ChatRepositoryInterface)
repo_provider.provide(AlchemyMessageRepository, provides=MessageRepositoryInterface)


use_case_provider = Provider(scope=Scope.REQUEST)
use_case_provider.provide_all(
    ShowChat,
    CreateChat,
    SendMessage,
    DeleteChat
)

container = make_async_container(DBProvider(), repo_provider, use_case_provider)
