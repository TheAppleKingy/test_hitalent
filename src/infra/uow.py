from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from src.application.interfaces.uow import UoWInterface, DomainEnt


class AlchemyUoW(UoWInterface):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._t: AsyncSessionTransaction = None  # type: ignore

    async def __aenter__(self) -> Self:
        self._t = await self._session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        self._t = None  # type: ignore
        return False

    async def commit(self) -> None:
        if self._t:
            await self._t.commit()

    async def rollback(self) -> None:
        if self._t:
            await self._t.rollback()

    def save(self, *ents: DomainEnt):
        return self._session.add_all(ents)
