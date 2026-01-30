from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator


StrippedStringType = Annotated[str, BeforeValidator(lambda x: x.strip())]


class ChatCreateDTO(BaseModel):
    title: StrippedStringType = Field(min_length=1, max_length=200)


class SendMessageDTO(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class ChatPreviewDTO(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageViewDTO(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatViewDTO(BaseModel):
    chat: Optional[ChatPreviewDTO]
    messages: list[MessageViewDTO]
