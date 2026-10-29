# CLAUDE.md - Developer Guidelines

## Build & Package Tooling
- Always use `uv` for environment, package, and dependency management.
- Add dependencies using `uv add` (or `uv add --dev` for testing tools).
- Always execute scripts and tools using the `uv run` prefix.

## Testing Standards (`pytest`)
- Tests reside in `tests/` matching `test_*.py`.
- Enforce the Given-When-Then layout using comments: `# Given:`, `# When:`, `# Then:`.
- Use descriptive snake_case names reflecting behavior (e.g., `test_install_adds_a_service`).
- Validate expected errors using `with pytest.raises(ExpectedError, match="exact error message"):`.
- Run the full test suite using `uv run pytest`.

## Code Style & Quality Gates
- Code formatting and linting: Run `uv run ruff format .` and `uv run ruff check . --fix`.
- Strict Type Safety: Every function, method, and return value must be fully annotated.
- Run `uv run mypy .\src\` to ensure static analysis passes before committing changes.
