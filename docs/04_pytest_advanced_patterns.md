# 04. Pytest II: Advanced Testing Patterns & Execution Filters

This document covers the architectural layout of professional test functions and precise test execution filtering.

---

## 🏗️ 1. The Given-When-Then Structure (Behavior-Driven Architecture)

A professional test should always be split into three distinct, readable sections to preserve clarity:

* **GIVEN (Arrange):** The initial state of the world. Setting up the data, mock entities, constants, variables, or system configurations required for the test.
* **WHEN (Act):** The specific action or operation being triggered. This usually involves invoking the single method or function under validation.
* **THEN (Assert):** The verification phase. Inspecting the final side effects, return values, or state mutations against the expected outcomes using native `assert` statements.

---

## 🔒 2. Precise Exception Handling (`pytest.raises`)

* Asserts that a block of code intentionally raises a specific built-in or custom exception.
* Captures the exception metadata into a reference container (`as exc_info`) to enable deep structural validation of the error text messages.

---

## ⚡ 3. Terminal Execution Filters: The `-k` Flag (Match Expressions)

Pytest allows you to bypass running the entire test suite by filtering tests at runtime using name-matching expressions via the `-k` flag:

```bash
# Runs only the tests whose names contain the word "eligibility"
uv run pytest -k "eligibility"

# Runs tests containing "gate" but excludes those containing "numeric"
uv run pytest -k "gate and not numeric"
```
---


