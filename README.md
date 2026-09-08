# PythonAdvancedLab

Personal laboratory for practicing advanced Python concepts, design patterns, and modern tooling.

## Prerequisites

This project is optimized to run in **GitHub Codespaces**. It uses **uv** for blazing-fast dependency management and virtual environment creation.

## Getting Started

If you are using GitHub Codespaces, the environment will automatically self-configure. If you are running it locally:

1. Install `uv` if you haven't already.
2. Create a virtual environment and install development dependencies:
   ```bash
   uv venv
   uv pip install -e .[dev]
   ```

## Project Quality Tools

We enforce high code quality using modern 2026 Python standards:
* **Linting & Formatting**: [Ruff](https://docs.astral.sh/ruff/)
* **Static Type Checking**: [Mypy](https://mypy-lang.org/) (Strict mode)
* **Testing**: [Pytest](https://docs.pytest.org/en/stable/)

To run tests:
```bash
pytest
```