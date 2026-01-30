from sqlalchemy import select, desc

from src.domain.entities import Message
from src.application.interfaces.repositories import MessageRepositoryInterface
from .alchemy import BaseAlchemyRepository


class AlchemyMessageRepository(BaseAlchemyRepository, MessageRepositoryInterface):
    async def get_by_chat(self, chat_id: int, limit: int) -> list[Message]:
        res = await self._session.scalars(
            select(Message).where(Message.chat_id == chat_id).order_by(desc(Message.created_at)).limit(limit)
        )
        return res.all()
