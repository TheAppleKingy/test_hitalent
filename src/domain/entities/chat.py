from dataclasses import dataclass, field
from datetime import datetime, timezone

from .message import Message


@dataclass
class Chat:
    title: str
    id: int = field(default=None, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)
    messages: list[Message] = field(default_factory=list, init=False)
