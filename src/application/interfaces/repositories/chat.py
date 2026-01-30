from typing import Protocol, Optional

from src.domain.entities import Chat


class ChatRepositoryInterface(Protocol):
    async def get_by_id(self, chat_id: int) -> Optional[Chat]: ...
    async def delete_chat(self, chat_id: int) -> None: ...
