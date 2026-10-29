# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Use `uv` for everything (envs, deps, running tools); prefix tool invocations with `uv run`.

```bash
uv add <pkg>                      # runtime dep;  uv add --dev <pkg> for dev tools
uv run pytest                     # full suite (testpaths = tests/)
uv run pytest tests/test_llm_engine/test_core.py::test_chat_callable_and_stateful_memory  # single test
uv run pytest -k "server"         # by name substring
uv run ruff format . && uv run ruff check . --fix
uv run mypy src                   # strict mode; must pass before committing
uv run python -m python_advanced_lab.main
```

Fresh setup (also what `.devcontainer` runs): `uv venv && uv pip install -e .[dev]`.

## Conventions

- Tests use Given-When-Then comments (`# Given:`, `# When:`, `# Then:`), behavior-describing snake_case names, and `pytest.raises(Err, match="exact message")` for error cases.
- mypy runs in `strict` mode over `src/` only — every function/method in `src/` needs full annotations. Tests are not type-checked (and some are unannotated).
- Ruff: line length 100, rules `E,F,B,I,UP`.

## Architecture

This is a learning lab, organized by **topic**. Each topic typically spans several parallel locations — keep them in sync when adding a new one:

| Topic | Code (`src/python_advanced_lab/`) | Tests (`tests/`) | Notes |
|---|---|---|---|
| Python data model / dunder protocols | `data_model/` | `test_data_model/` | `docs/01`, `docs/02`, `exercises/data_model/` |
| Pytest patterns | `testing_lab/` | `test_pytest_fundamentals/` | `docs/03`, `docs/04` |
| Ollama chat engine | `llm_engine/core.py` | `test_llm_engine/` | `docs/02`, `notebooks/` |
| Claude Code agent config | — | — | `docs/05` |

`docs/NN_*.md` are numbered theory notes; subpackage `README.md` files are concept references. `pipeline.py` / `main.py` are small standalone practice scripts, and `pipeline.py` contains deliberately non-idiomatic code (e.g. `range(len(...))`, a redundant `file.close()`), so ask before "fixing" it.

### `llm_engine.Chat`

`Chat` is a stateful wrapper around `ollama.chat`. It shows protocols in use: `__call__` sends a turn and adds it to history, `__len__`/`__getitem__` (with `@overload` for int vs slice) index the message history, `__contains__` does a case-insensitive content search, and `__enter__`/`__exit__` act as a session context manager.
- The system prompt is not stored in `_messages`; it is put in front of every request payload.
- `__exit__` writes `transcript.txt` to the **current working directory**.
- The default model is `qwen2.5:14b`. The notebooks need a local Ollama server, but the tests don't, because they mock it with `@patch("ollama.chat")`.
- `llm_engine/` has no `__init__.py`, so it is a namespace package.

### Gotchas

- `Server` is defined twice with different signatures: `data_model/operators.py` (name, os, version) and `testing_lab/inventory.py` (also takes a services list). Import the one that matches the topic.
- `pyproject.toml` declares dev tools in two places: `[dependency-groups].dev` (pytest, ipykernel, ruff) and `[project.optional-dependencies].dev` (pytest, ruff, mypy). mypy is only in the optional extra.
- `requires-python >= 3.13`, but ruff/mypy target 3.12.
