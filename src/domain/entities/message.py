from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Message:
    chat_id: int
    text: str
    id: int = field(default=None, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)
