"""
    Unit tests for callable and context manager lifecycle boundaries.
"""

import pytest
from python_advanced_lab.data_model.call_context import SecureRunner


def test_secure_runner_lifecycle() -> None:
    runner = SecureRunner(runner_id="runner-42")

    # Guard clause verification (Blocked outside context)
    with pytest.raises(RuntimeError, match="Execution blocked"):
        runner("git status")

    # Active context block execution
    with runner as pipeline:
        assert pipeline.is_active is True
        output = pipeline("  uv run pytest  ")
        assert "success executing" in output.lower()
        assert "uv run pytest" in pipeline.execution_history

    # Post-context execution teardown verification
    assert runner.is_active is False
    with pytest.raises(RuntimeError):
        runner("git push")
