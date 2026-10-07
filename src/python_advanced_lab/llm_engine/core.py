"""
    Core module implementing a stateful, protocol-driven Ollama LLM interface.
"""

from types import TracebackType
from typing import Any, Literal, TypedDict, Union, overload
import ollama


class ChatMessage(TypedDict):
    """
        Type definition for structured chat messages expected by Ollama.
    """
    role: Literal["system", "user", "assistant"]
    content: str


class Chat:
    """
        Stateful wrapper for Ollama chat completions utilizing data model protocols.
    """

    def __init__(
        self,
        model: str = "qwen2.5:14b",
        system: str = "Answer in English, in a single sentence.",
    ) -> None:
        self.model: str = model
        self.system: str = system
        self._messages: list[ChatMessage] = []

    def __call__(self, text: str) -> str:
        """
            Enables the chat instance to be invoked directly as a function.
        """
        self._messages.append({"role": "user", "content": text})
        
        # Prepare the payload with the initial system prompt boundary
        payload: list[ChatMessage] = [{"role": "system", "content": self.system}]
        payload.extend(self._messages)
        
        response = ollama.chat(model=self.model, messages=payload)  
        content: str = response.message.content or ""
        
        self._messages.append({"role": "assistant", "content": content})
        return content

    def __repr__(self) -> str:
        return f"Chat(model={self.model!r}, messages={len(self._messages)})"

    def __str__(self) -> str:
        labels: dict[str, str] = {"user": "you", "assistant": self.model}
        return "\n".join(
            f"{labels.get(m['role'], 'unknown')}: {m['content']}"
            for m in self._messages
        )

    def __len__(self) -> int:
        return len(self._messages)

    @overload
    def __getitem__(self, index: int) -> ChatMessage: ...

    @overload
    def __getitem__(self, index: slice) -> list[ChatMessage]: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[ChatMessage, list[ChatMessage]]:
        return self._messages[index]

    def __contains__(self, item: str) -> bool:
        return any(item.lower() in m["content"].lower() for m in self._messages)

    def __enter__(self) -> "Chat":
        print(f"[open session with {self.model}]")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        with open("transcript.txt", "w", encoding="utf-8") as file:
            file.write(str(self))
        print(f"[closed session: {len(self)} messages saved to transcript.txt]")
        return False
