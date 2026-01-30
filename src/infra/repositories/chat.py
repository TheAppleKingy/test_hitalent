from typing import Optional

from sqlalchemy import select, delete

from src.domain.entities import Chat
from src.application.interfaces.repositories import ChatRepositoryInterface
from .alchemy import BaseAlchemyRepository


class AlchemyChatRepository(BaseAlchemyRepository, ChatRepositoryInterface):
    async def get_by_id(self, chat_id: int) -> Optional[Chat]:
        return await self._session.scalar(select(Chat).where(Chat.id == chat_id))

    async def delete_chat(self, chat_id: int) -> None:
        await self._session.execute(delete(Chat).where(Chat.id == chat_id))
