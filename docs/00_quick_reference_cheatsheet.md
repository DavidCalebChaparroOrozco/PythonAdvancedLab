# Laboratory Quick Reference Cheatsheet

A centralized command guide covering package management (`uv`), code quality gates (`ruff`, `mypy`, `pytest`), container orchestration (`docker compose`), and Git workflows used across **PythonAdvancedLab**.

---

## 📦 1. Environment & Dependency Management (`uv`)

| Action | Command | Description |
| :--- | :--- | :--- |
| **Create Virtual Env** | `uv venv` | Initializes an isolated local `.venv` directory. |
| **Install Editable Pkg** | `uv pip install -e .[dev]` | Installs the `src/` layout package locally with dev tools. |
| **Add Runtime Dep** | `uv add <package>` | Installs a production package and updates `pyproject.toml` / `uv.lock`. |
| **Add Dev Dep** | `uv add --dev <package>` | Installs a development-only package (e.g., `pytest`, `ruff`). |
| **Run Module** | `uv run python -m python_advanced_lab.<module>` | Executes a package module using the managed virtual environment. |

---

## 🧪 2. Testing & Quality Gates (`pytest`, `mypy`, `ruff`)

| Tool / Action | Command | Description |
| :--- | :--- | :--- |
| **Run All Tests** | `uv run pytest -v` | Discovers and executes the full test suite in verbose mode. |
| **Run Single Test File** | `uv run pytest tests/<folder>/<test_file>.py` | Runs tests inside a specific module file. |
| **Filter Tests (`-k`)** | `uv run pytest -k "<keyword> and not <other>"` | Runs tests matching boolean keyword expressions. |
| **Strict Type Check** | `uv run mypy src` | Validates strict static type annotations across `src/`. |
| **Format & Lint** | `uv run ruff format . && uv run ruff check . --fix` | Auto-formats code style and fixes linting warnings. |

---

## 🐳 3. Container Infrastructure (`docker compose`)

| Action | Command | Description |
| :--- | :--- | :--- |
| **Validate Compose File**| `docker compose config` | Checks `compose.yaml` syntax and resolves build paths. |
| **Build & Start Fleet** | `docker compose up -d --build` | Builds server images (`etl-01`, `db-01`, `web-01`) and runs them in background. |
| **Check Container Status**| `docker compose ps` | Lists active containers and their current runtime states. |
| **Run Bastion Script** | `docker compose --profile tools run --rm -e PYTHONPATH=src bastion python -m <module>` | Launches an ephemeral `bastion` container to run Python scripts inside the Docker network. |
| **Stop & Clean Fleet** | `docker compose down` | Stops and removes all running lab containers and networks. |

---

## 🔀 4. Git Feature-Branch Workflow

| Stage | Command | Description |
| :--- | :--- | :--- |
| **Start Feature Branch** | `git checkout main && git pull origin main && git checkout -b feature/<topic>` | Syncs `main` and creates an isolated working branch. |
| **Check Workspace** | `git status` | Inspects modified, staged, and untracked files. |
| **Semantic Commit** | `git add <files> && git commit -m "<type>(<scope>): <message>"` | Records atomic changes (`feat`, `docs`, `chore`, `test`, `refactor`). |
| **Integrate to Main** | `git checkout main && git merge feature/<topic> --no-ff -m "merge: <summary>"` | Merges feature work back into `main` preserving branch history. |
| **Clean Up Branches** | `git branch -d feature/<topic> && git push origin --delete feature/<topic>` | Deletes temporary branches both locally and on GitHub. |
