# 05. AI Agent Governance: CLAUDE.md & Lifecycle Hooks

This document explores how to establish deterministic boundaries and context injection for AI coding agents (such as Claude Code) operating within a professional codebase.

---

## 📘 1. The CLAUDE.md Specification
* **Purpose:** Provides definitive, high-priority context directly to the AI agent regarding project rules, build commands, testing strategies, and code styling standards.
* **Location:** Must always reside at the absolute root of the repository.
* **Core Philosophy:** While a prompt suggests guidelines, `CLAUDE.md` forces alignment by explicitly showing the agent the exact toolchains used (e.g., `uv`, `pytest`, `ruff`).

---

## 🔒 2. Deterministic Hooks Layer
* **Concept:** Shell commands or scripts triggered at specific lifecycle events of the agent session (e.g., `SessionStart`, `PreToolUse`, `PostToolUse`).
* **Non-Interpretive Nature:** Unlike text prompts, hooks are non-negotiable. They are executed directly by the system shell. The AI does not interpret them; it must comply with their pass/fail exit codes.
* **Safety Gate:** Used to prevent destructive actions, protect environment variables (`.env`), or auto-format code edits via `ruff` post-generation.

---

## 📊 3. Crucial Lifecycle Events
* `InstructionsLoaded`: Fires when `CLAUDE.md` is loaded into the context.
* `PreToolUse`: Triggers before the agent executes a shell command or tool. Ideal for blocking hazardous execution strings.
* `PostToolUse`: Triggers after a tool executes. Perfect for running `uv run ruff format` or validation suites.

---

## What We’ll Cover Today

- The Problem: An AI agent can modify our code, but how much does it know about our project, and what could it accidentally break?

- CLAUDE.md: A project instruction file that explains what the project does, where it is heading, how code should be written, and what rules or limitations the agent must follow.

- Hooks: Commands or scripts that run automatically when specific events occur. We’ll explore events, matchers, `settings.json`, and how they work together in Claude Code.

- Our Two Hooks:
  - Automatic formatting: Run Ruff after every code edit to keep the code consistently formatted.
  - Verification before finishing: Run Ruff and `pytest` to check code quality and ensure tests pass before the agent finishes its work.

- CLAUDE.md vs. Hooks: Understand the difference between instructions that ask an agent to follow certain rules and automated checks that enforce those rules. Learn when to use each.

> Core Concept: Some rules are requested, while others are enforced automatically. Instructions guide the agent's behavior; hooks help ensure specific actions or checks happen at the right time.

---

## What Is Claude Code?

Claude Code is an AI-powered programming agent that works directly within a software project.

How it works: You interact with it using natural language. You describe what you want to accomplish, and it examines the project, reads the relevant code, determines what needs to be done, and makes the necessary changes.

## Two Important Questions

### 1. How Does Claude Code Know How We Work on the Project?

For example, how does it know that:

- We use `uv` instead of `pip` to manage Python dependencies.
- Tests are stored in the `tests/` directory.
- We follow the Given-When-Then pattern when writing tests.

The answer: `CLAUDE.md`.

This file contains project-specific instructions that guide Claude Code's behavior, including coding conventions, tools, testing practices, and project structure.

Each new session starts without the full context of previous conversations. Claude Code can, however, inspect the project files and read `CLAUDE.md` to understand the project's rules and conventions.

### 2. How Do We Ensure Claude Code Doesn't Break Anything?

We want to ensure that:

- Code follows the project's formatting and style rules.
- Tests continue to pass after every change.
- These checks run consistently, rather than depending on the agent to remember to perform them.

The answer: Hooks.

Hooks are automated actions triggered by specific events during Claude Code's workflow. They can run formatters, execute tests, validate code, or perform other checks at predefined points.

Unlike instructions in `CLAUDE.md`, which tell the agent what it should do, hooks can enforce specific actions automatically when their configured events occur.

In short:

- `CLAUDE.md` tells Claude Code how to work on the project.
- Hooks automate checks and actions to help maintain code quality and consistency.

---

## What Is the `CLAUDE.md` File For?

`CLAUDE.md` is a Markdown file that provides project-specific instructions to Claude Code. It explains how the project is organized, which tools to use, what coding conventions to follow, and how to test changes.

It acts as a set of guidelines for the AI agent, helping it work consistently with the project's requirements.

## Where Does It Go? Three Possible Locations

The file's location determines its scope: whether the instructions apply to multiple projects, a specific project, or only your personal workflow.

### 1. Personal instructions

```
~/.claude/
└── CLAUDE.md
```

Applies to your projects by default, providing general preferences such as coding style, tools, and common workflows.

### 2. Project instructions

```
project_n/
├── CLAUDE.md
└── .claude/
    ├── CLAUDE.md
    └── settings.json
```

- `CLAUDE.md`: Contains instructions shared with the project team.
- `.claude/CLAUDE.md`: Can provide additional instructions in a subdirectory. It is not a universal alternative location for the root instructions file; Claude Code supports nested `CLAUDE.md` files within project directories.
- `.claude/settings.json`: Stores project-level settings, including hook configurations.

### 3. Personal project instructions

```
project_n/
└── CLAUDE.local.md
```

Contains personal instructions specific to the project that you do not want to share with the team. Add `CLAUDE.local.md` to `.gitignore` to prevent it from being committed to version control.

These locations can be combined. Claude Code can load applicable instruction files from the project and its parent directories, as well as personal instructions. The exact files loaded depend on their location and the context in which Claude Code is launched.

## What Should You Write in `CLAUDE.md`?

Write specific, clear, and verifiable instructions rather than vague recommendations.

| Instead of writing...        | Write...                                     |
| ---------------------------- | -------------------------------------------- |
| "Format the code correctly." | "Use 2-space indentation."                   |
| "Test the changes."          | "Run `npm test` before committing."          |
| "Keep files organized."      | "Place API handlers in `src/api/handlers/`." |

### Best practices

- Be concise: Keep the file short, ideally under 200 lines, so the instructions are easier to follow and consume less context.
- Stay organized: Use Markdown headings (`##`) and bullet points (`-`) to group related instructions.
- Avoid contradictions: Conflicting instructions can cause inconsistent behavior. Keep the rules clear and consistent.
- Make instructions actionable: Specify which commands to run, where files belong, and what conditions must be satisfied.

## Our `CLAUDE.md` Example

The following file defines the tools, testing conventions, and coding standards for the `PythonAdvancedLab 2026` project.

```text
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
```

### What does each section accomplish?

- Project: Identifies the project and its main component.
- Tools: Specifies how to manage dependencies and execute commands, ensuring the agent follows the project's Python environment conventions.
- Tests: Defines test locations, naming conventions, structure, error-handling expectations, and when tests are required.
- Style: Specifies a code-quality check that should be performed before finishing.

The instructions apply to the AI agent as well as its work on the codebase. For example, when modifying `inventory.py`, Claude Code should add a corresponding test and run the test suite using `uv run pytest`.

Key idea: `CLAUDE.md` tells Claude Code what rules and conventions to follow. It provides guidance, but it does not automatically enforce every rule. For checks that must run consistently, configure hooks or other automated quality-control tools.

---

## Two Useful Commands: `/init` and `/context`

Claude Code provides two commands that help us create project instructions and verify whether they are loaded into the current session.

### 1. `/init` — Creates an Initial `CLAUDE.md`

The `/init` command analyzes the project and generates an initial `CLAUDE.md` file containing relevant information, such as project structure, development commands, and coding conventions.

It is a useful starting point, but the generated file should be reviewed and adjusted to ensure its instructions are accurate.

If a `CLAUDE.md` file already exists, Claude Code can use the existing instructions as a starting point and suggest improvements rather than simply replacing them.

### 2. `/context` — Shows the Current Context

The `/context` command displays information about the context available to Claude Code in the current session, including how much context is being used.

Use it to check whether your project instructions have been loaded and how much context they occupy.

The `/memory` command provides access to memory-related instructions and settings, allowing you to manage relevant instruction files.

## The Limitation: Context Is Not the Same as Enforcement

A `CLAUDE.md` file provides instructions, but it does not guarantee that Claude Code will execute every requested action on every task.

Consider this instruction:

```
## Style
- Run `uv run ruff check .` before finishing.
```

### Step 1: Claude follows the instruction

You ask Claude Code to add an `uninstall()` method to `inventory.py`.

Claude reads the instructions, implements the method, and runs the linter.

```
Task: Add uninstall()
Edit: inventory.py
Run: uv run ruff check .
Result: All checks passed.
```

This is the expected behavior.

### Step 2: Claude follows the instruction again

You ask it to validate a version.

```
Task: Validate the version
Edit: inventory.py
Run: uv run ruff check .
Result: All checks passed.
```

The instruction appears to work consistently.

### Step 3: Claude misses the instruction

You assign a larger refactoring task that involves multiple files and consumes substantial context.

```
Task: Extensive refactoring
Edit: inventory.py (multiple changes)
Edit: tests/test_servidor.py
Result: Task completed without running Ruff.
```

Even though the instruction remains in `CLAUDE.md`, Claude may finish without executing the required check. The instruction guides its decisions; it does not independently enforce the command.

This is an illustrative scenario, not a guarantee that longer tasks will cause Claude to skip checks.

### Step 4: The key distinction

The difference is between telling an agent what to do and automatically enforcing that it happens.

| `CLAUDE.md`                                     | Hooks                                                              |
| ----------------------------------------------- | ------------------------------------------------------------------ |
| Provides instructions and guidelines.           | Automatically runs configured actions when specified events occur. |
| Relies on the agent to follow the instructions. | Can enforce checks at predefined workflow points.                  |
| Helps the agent understand project conventions. | Helps ensure required validations are performed consistently.      |

For example, if Ruff must run after every file edit or before a task finishes, a suitable hook can trigger the command automatically at the configured event. The hook must be configured correctly, and its scope must cover the actions you want to enforce.

Key principle: Use `CLAUDE.md` to explain how Claude Code should work. Use hooks and other automated checks when an action must happen consistently, regardless of the agent's decisions.

---

## Hooks

### What Are Hooks?

Hooks are automated actions that run when specific events occur during Claude Code's workflow.

A hook connects an event to a command or other action, allowing us to automate tasks such as formatting code, running tests, and validating changes without relying entirely on Claude to remember to do them.

## How Hooks Work

### Step 1: The Agent's Workflow

Claude Code follows a cycle: it receives a prompt, decides what to do, uses tools such as `Edit` or `Bash`, evaluates the results, and eventually responds to the user.

Hooks can be attached to specific events throughout this process.

### Step 2: `SessionStart` — When a Session Begins

This event occurs when a Claude Code session starts.

You can use it to perform initialization tasks, such as displaying project information, loading relevant context, or running setup commands.

### Step 3: `PreToolUse` — Before a Tool Is Used

This event occurs immediately before Claude Code executes a tool.

You can use it to validate an action before it happens. Depending on the hook's response, the action can be allowed, blocked, or require additional handling.

For example, a hook could prevent Claude from executing a prohibited command.

### Step 4: `PostToolUse` — After a Tool Is Used

This event occurs after a tool finishes executing successfully.

You can use it to automate follow-up actions, such as formatting a file after Claude edits it.

For example, after an edit to a Python file, a hook could run Ruff to format the modified file automatically.

### Step 5: `Stop` — When Claude Finishes Responding

This event occurs when Claude Code is about to finish its response.

You can use it to run final verification checks, such as checking code style and executing tests.

For example, a hook could run Ruff and pytest before allowing the workflow to finish. If the hook blocks completion when checks fail, Claude can be prompted to continue working and fix the problems.

Important distinction: Hooks automate actions at predefined events, but they do not guarantee that every possible problem will be detected. Their effectiveness depends on how they are configured and which checks they perform.

## Configuration and Loading

Hooks are configured in JSON settings files. The file's location determines whether the hooks apply to all your projects, a specific shared project, or only your local copy of a project.



| File location                 | Scope                                                           |
| ----------------------------- | --------------------------------------------------------------- |
| `~/.claude/settings.json`     | Applies across your projects.                                   |
| `.claude/settings.json`       | Applies to the current project and can be shared with the team. |
| `.claude/settings.local.json` | Applies to the current project for your personal use.           |

### Example: Automatically Format Code After an Edit

The following configuration runs Ruff's formatter whenever Claude Code uses the `Edit` or `Write` tool.

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run ruff format ."
          }
        ]
      }
    ]
  }
}
```

This file should be saved as `.claude/settings.json` in the project root.

### How It Works

1. `hooks` defines the hooks configuration.
2. `PostToolUse` specifies that the hook runs after a tool executes successfully.
3. `matcher: "Edit|Write"` matches either the `Edit` or `Write` tool.
4. `type: "command"` specifies that the hook executes a shell command.
5. `command` defines the command to run: `uv run ruff format .`.

In plain language: whenever Claude Code successfully edits or writes a file, it automatically runs Ruff's formatter across the project.

Important: This example formats the entire project after each matching tool call, which can be inefficient. Also, `ruff format .` formats code but does not check all linting rules. For more targeted formatting, configure the hook to format only the modified Python file. Use `uv run ruff check .` separately to check for linting issues.

The `PostToolUse` event does not block the completed edit if formatting fails. If you need to prevent Claude from finishing until checks pass, configure an appropriate verification hook, such as `Stop`, to enforce that behavior.

---

## How a Hook Communicates with Claude Code

A hook is a program that receives information from Claude Code, performs a specific action, and returns a result. This allows Claude Code to react to the hook's outcome.

### Step 1: Claude Code Sends Information to the Hook

When a configured event occurs, Claude Code provides the hook with information about that event through standard input (`stdin`), typically as a JSON object.

For example, when the `Stop` event occurs, Claude Code might send data like this:

```
{
  "hook_event_name": "Stop",
  "cwd": "/home/PythonAdvancedLab/",
  "stop_hook_active": false,
  "session_id": "...",
  "transcript_path": "..."
}
```

Each field provides information about the current execution:

- `hook_event_name`: The event that triggered the hook.
- `cwd`: The current working directory.
- `stop_hook_active`: Indicates whether a stop hook is already active in the current stopping process.
- `session_id`: Identifies the current session.
- `transcript_path`: Provides the path to the conversation transcript.

The hook can read this information to determine what action to perform.

### Step 2: The Hook Executes Its Logic

Suppose the hook is a Python script named `check.py`. It could inspect the project, run tests, or check whether the code meets specific requirements.

For example, it could run `uv run ruff check .` and `uv run pytest` to validate the code before Claude Code finishes.

### Step 3: The Hook Returns a Result

The hook communicates its result through its exit code, standard error (`stderr`), and, when applicable, structured JSON output.

For a command-based `Stop` hook, the important outcomes are:

- Exit code `0`: The hook completed successfully. Any decision to allow or block stopping depends on the event-specific output and rules.
- Exit code `2`: Indicates a blocking error. For a `Stop` hook, this prevents Claude Code from stopping and provides feedback for further action.
- Other nonzero exit codes: Generally indicate an error, but do not automatically block every hook event.

`stderr` can provide diagnostic information. For a `Stop` hook, simply printing an error message is not equivalent to explicitly blocking completion; the hook must use the appropriate mechanism.

Key idea: Claude Code sends event information to the hook, the hook performs its checks, and its result determines what happens next according to the rules for that event.

## `CLAUDE.md` vs. Hooks: Requesting vs. Enforcing

These mechanisms serve different purposes and work best together.

| Aspect                   | `CLAUDE.md`                                    | Hooks                                                |
| ------------------------ | ---------------------------------------------- | ---------------------------------------------------- |
| What it is               | A file containing instructions                 | Executable commands triggered by events              |
| Who decides what happens | Claude interprets and follows the instructions | The configured event triggers the hook automatically |
| Best for                 | Project conventions, context, and workflows    | Automated checks and required actions                |
| Example                  | "Use the Given-When-Then pattern for tests."   | "Run `pytest` when Claude attempts to finish."       |

### What Should Go in Each?

Use `CLAUDE.md` for requirements that require interpretation or judgment.

For example:

- Use meaningful test names.
- Follow the Given-When-Then pattern.
- Keep functions focused on a single responsibility.
- Follow the project's architecture.

These requirements can be difficult to verify with a simple command because they involve understanding the code.

Use hooks for requirements that can be automated and must be checked consistently.

For example:

- Run Ruff to check code quality.
- Run pytest to verify that tests pass.
- Prevent prohibited commands from executing.
- Automatically format modified files.

Some rules can use both mechanisms. `CLAUDE.md` can explain the required convention, while a hook or other automated tool checks compliance.

For instance, `CLAUDE.md` can explain how tests should follow Given-When-Then, while a custom validation script checks whether the required comment markers are present. Such a script would enforce only the specific conditions it was designed to recognize.

### Rule of Thumb

If an instruction in `CLAUDE.md` can be converted into a reliable automated check, and it is critical that the check always runs, consider implementing it as a hook.

Use `CLAUDE.md` to guide Claude's decisions and hooks to automate enforcement.