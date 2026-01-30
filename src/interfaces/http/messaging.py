from fastapi import APIRouter, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.dtos import ChatCreateDTO, ChatPreviewDTO, SendMessageDTO, ChatViewDTO, MessageViewDTO
from src.application.use_cases import *

chat_couter = APIRouter(prefix="/chats", tags=["Chats router"], route_class=DishkaRoute)


@chat_couter.post("")
async def create_chat(dto: ChatCreateDTO, use_case: FromDishka[CreateChat]) -> ChatPreviewDTO:
    return await use_case.execute(dto)


@chat_couter.post("/{chat_id}/messages")
async def send_message(chat_id: int, dto: SendMessageDTO, use_case: FromDishka[SendMessage]) -> MessageViewDTO:
    return await use_case.execute(chat_id, dto)


@chat_couter.get("/{chat_id}")
async def get_chat_messages(
    chat_id: int,
    use_case: FromDishka[ShowChat],
    limit: int = Query(default=20, le=100),
) -> ChatViewDTO:
    chat, messages = await use_case.execute(chat_id, limit)
    return ChatViewDTO(chat=chat, messages=messages)


@chat_couter.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: int, use_case: FromDishka[DeleteChat]) -> None:
    return await use_case.execute(chat_id)
