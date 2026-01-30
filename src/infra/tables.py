from datetime import datetime, timezone

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import TEXT


def id_():
    return Column('id', Integer, primary_key=True, autoincrement=True)


metadata = MetaData()

chats = Table(
    "chats", metadata,
    id_(),
    Column("title", String(200), nullable=False, unique=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    CheckConstraint("length(title) >= 1")
)

messages = Table(
    "messages", metadata,
    id_(),
    Column("chat_id", ForeignKey("chats.id", ondelete="CASCADE"), nullable=False),
    Column("text", TEXT, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    CheckConstraint("length(text) >= 1")
)
