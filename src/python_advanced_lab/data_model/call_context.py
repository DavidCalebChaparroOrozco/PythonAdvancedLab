"""
    Module practicing Callable instances and safe Context Manager protocols.
"""

from types import TracebackType
from typing import Literal, Self


class SecureRunner:
    """
        Combines high-order function emulation with context environmental boundaries.
    """

    def __init__(self, runner_id: str) -> None:
        self.runner_id: str = runner_id
        self.is_active: bool = False
        self.execution_history: list[str] = []

    def __enter__(self) -> Self:
        """Prepares the clean execution sandbox."""
        self.is_active = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """
            Safely dismantles the environment state and forces exception transparency.
        """
        self.is_active = False
        # Return False to ensure exceptions are never silenced silently in production
        return False

    def __call__(self, pipeline_command: str) -> str:
        """
            Allows instances to act exactly like an advanced stateful executable function.
        """
        if not self.is_active:
            raise RuntimeError("Execution blocked. Runner context is not active.")
        
        clean_command = pipeline_command.strip().lower()
        self.execution_history.append(clean_command)
        return f"[{self.runner_id}] Success executing: {clean_command}"
