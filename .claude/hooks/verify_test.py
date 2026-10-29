"""
Deterministic agent lifecyle stop hook to enforce quality gates before session teardown.
"""

import json
import subprocess
import sys
from typing import Any


def run_verification_pipeline() -> None:
    """
    Parses agent state via stdin and executes strict ruff and pytest quality gates.
    """
    # Safe parsing of the agent session event dictionary payload
    entry: dict[str, Any] = json.load(sys.stdin)

    # Bypass clause if the stop hook explicitly passes an active flag
    if entry.get("stop_hook_active"):
        sys.exit(0)

    # Automated verification matrix commands
    commands: list[list[str]] = [
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "pytest", "-q"],
    ]

    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            # Route stdout feedback back into stderr so the AI agent can read the crash report
            print(result.stdout, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    run_verification_pipeline()
