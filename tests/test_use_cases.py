import pytest
from unittest.mock import AsyncMock, Mock, MagicMock
from datetime import datetime
from src.application.interfaces import UoWInterface
from src.application.interfaces.repositories import *
from src.application.dtos import ChatCreateDTO, SendMessageDTO
from src.application.use_cases import *
from src.domain.entities import *
from src.application.errors import ChatNotFound


@pytest.mark.asyncio
async def test_create_chat_saves_and_returns_chat():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = False
    mock_uow.save = MagicMock()
    mock_uow.commit = AsyncMock()

    use_case = CreateChat(mock_uow)
    dto = ChatCreateDTO(title="Test Chat")

    # Act
    result = await use_case.execute(dto)

    # Assert
    assert result.title == "Test Chat"
    mock_uow.save.assert_called_once_with(result)
    mock_uow.__aenter__.assert_called_once()
    mock_uow.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_create_chat_handles_save_exception():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = False
    mock_uow.save.side_effect = ValueError("Save failed")

    use_case = CreateChat(mock_uow)
    dto = ChatCreateDTO(title="Test Chat")

    with pytest.raises(ValueError, match="Save failed"):
        await use_case.execute(dto)

    mock_uow.save.assert_called_once()
    mock_uow.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_send_message_creates_and_saves_message():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.save = MagicMock()

    mock_chat_repo = AsyncMock(spec=ChatRepositoryInterface)
    chat = Chat("test")
    chat.id = 42
    mock_chat_repo.get_by_id.return_value = chat

    use_case = SendMessage(mock_uow, mock_chat_repo)
    dto = SendMessageDTO(text="Hello world")

    result = await use_case.execute(chat_id=42, dto=dto)

    assert result.chat_id == 42
    assert result.text == "Hello world"
    mock_chat_repo.get_by_id.assert_called_once_with(42)
    mock_uow.save.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_send_message_raises_when_chat_not_found():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow

    mock_chat_repo = AsyncMock(spec=ChatRepositoryInterface)
    mock_chat_repo.get_by_id.return_value = None

    use_case = SendMessage(mock_uow, mock_chat_repo)
    dto = SendMessageDTO(text="Hello world")

    with pytest.raises(ChatNotFound, match="Chat not fount"):
        await use_case.execute(chat_id=99, dto=dto)

    mock_chat_repo.get_by_id.assert_called_once_with(99)
    mock_uow.save.assert_not_called()


@pytest.mark.asyncio
async def test_show_chat_returns_chat_and_messages_when_found():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow

    mock_chat_repo = AsyncMock()
    chat = Chat("test")
    chat.id = 42
    mock_chat_repo.get_by_id.return_value = chat
    mock_message_repo = AsyncMock()
    mock_message_repo.get_by_chat.return_value = [Message(42, "msg1"), Message(42, "msg2")]

    use_case = ShowChat(mock_uow, mock_chat_repo, mock_message_repo)

    result = await use_case.execute(chat_id=42, limit=10)

    chat, messages = result
    assert chat.id == 42
    assert len(messages) == 2
    assert all(m.chat_id == 42 for m in messages)
    mock_chat_repo.get_by_id.assert_called_once_with(42)
    mock_message_repo.get_by_chat.assert_called_once_with(42, 10)


@pytest.mark.asyncio
async def test_show_chat_returns_empty_when_chat_not_found():
    mock_uow = AsyncMock(spec=UoWInterface)
    mock_uow.__aenter__.return_value = mock_uow

    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_by_id.return_value = None

    mock_message_repo = AsyncMock()

    use_case = ShowChat(mock_uow, mock_chat_repo, mock_message_repo)

    result = await use_case.execute(chat_id=99, limit=10)

    chat, messages = result
    assert chat is None
    assert messages == []
    mock_chat_repo.get_by_id.assert_called_once_with(99)
    mock_message_repo.get_by_chat.assert_not_called()
