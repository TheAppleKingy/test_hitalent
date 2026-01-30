from typing import Protocol

from src.domain.entities import Message


class MessageRepositoryInterface(Protocol):
    async def get_by_chat(self, chat_id: int, limit: int) -> list[Message]: ...
