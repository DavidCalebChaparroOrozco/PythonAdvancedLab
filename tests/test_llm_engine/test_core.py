"""
    Unit tests validating the protocol-driven Ollama Chat engine functionality.
"""

from unittest.mock import MagicMock, patch
import pytest
from python_advanced_lab.llm_engine.core import Chat


@pytest.fixture
def mock_ollama_response() -> MagicMock:
    """
        Creates a standardized mock response mimicking the Ollama API structure.
    """
    mock_res = MagicMock()
    mock_res.message.content = "Oslo is the capital of Norway."
    return mock_res


@patch("ollama.chat")
def test_chat_callable_and_stateful_memory(mock_chat: MagicMock, mock_ollama_response: MagicMock) -> None:
    """
        Validates that __call__ appends messages and routes payloads correctly.
    """
    # Given
    mock_chat.return_value = mock_ollama_response
    chat = Chat(model="qwen2.5:14b")

    # When
    response = chat("What is the capital of Norway?")

    # Then
    assert response == "Oslo is the capital of Norway."
    assert len(chat) == 2  # One user message, one assistant response
    assert chat[0]["role"] == "user"
    assert chat[1]["role"] == "assistant"


@patch("ollama.chat")
def test_chat_collection_protocols(mock_chat: MagicMock, mock_ollama_response: MagicMock) -> None:
    """
        Ensures len, getitem, and contains work harmoniously as a collection.
    """
    mock_chat.return_value = mock_ollama_response
    chat = Chat()
    
    chat("Query sample")

    # Test __len__
    assert len(chat) == 2

    # Test __contains__ (Case-insensitive verification)
    assert "query" in chat
    assert "oslo" in chat
    assert "bogota" not in chat

    # Test __getitem__ slicing emulation
    sliced_messages = chat[:]
    assert len(sliced_messages) == 2
    assert isinstance(sliced_messages, list)


@patch("ollama.chat")
def test_context_manager_transcript_lifecycle(
    mock_chat: MagicMock, mock_ollama_response: MagicMock, tmp_path: pytest.TempPathFactory
) -> None:
    """
        Validates __enter__ and __exit__ execution context behavior.
    """
    mock_chat.return_value = mock_ollama_response

    # Force writing transcript to a safe test directory instead of project root
    with patch("builtins.open", patch("builtins.open").new) as mock_open:
        with Chat() as active_chat:
            active_chat("Hello agent")
            assert len(active_chat) == 2

    # Verification of clean exit status
    assert len(active_chat) == 2
