from typing import Optional

from src.domain.entities import Chat, Message
from src.application.interfaces import UoWInterface
from src.application.interfaces.repositories import *
from src.application.dtos import ChatCreateDTO, SendMessageDTO
from .errors import ChatNotFound

__all__ = [
    "CreateChat",
    "SendMessage",
    "ShowChat",
    "DeleteChat"
]


class CreateChat:
    def __init__(self, uow: UoWInterface):
        self._uow = uow

    async def execute(self, dto: ChatCreateDTO):
        async with self._uow as uow:
            created = Chat(dto.title)
            uow.save(created)
        return created


class SendMessage:
    def __init__(self, uow: UoWInterface, chat_repo: ChatRepositoryInterface):
        self._uow = uow
        self._chat_repo = chat_repo

    async def execute(self, chat_id: int, dto: SendMessageDTO):
        async with self._uow as uow:
            chat = await self._chat_repo.get_by_id(chat_id)
            if not chat:
                raise ChatNotFound("Chat not fount")
            message = Message(chat.id, dto.text)
            uow.save(message)
        return message


class ShowChat:
    def __init__(
            self,
            uow: UoWInterface,
            chat_repo: ChatRepositoryInterface,
            message_repo: MessageRepositoryInterface
    ):
        self._uow = uow
        self._chat_repo = chat_repo
        self._message_repo = message_repo

    async def execute(self, chat_id: int, limit: int) -> tuple[Optional[Chat], list[Message]]:
        async with self._uow:
            chat = await self._chat_repo.get_by_id(chat_id)
            if not chat:
                return None, []
            return chat, await self._message_repo.get_by_chat(chat_id, limit)


class DeleteChat:
    def __init__(self, uow: UoWInterface, chat_repo: ChatRepositoryInterface):
        self._uow = uow
        self._chat_repo = chat_repo

    async def execute(self, chat_id: int):
        async with self._uow:
            return await self._chat_repo.delete_chat(chat_id)
