# Pytest: The First Test — `assert`, Discovery, and Introspection

## What is an automated test?

An automated test is code that checks whether another piece of code behaves as expected. Instead of manually checking the result every time, the test verifies it automatically.

### Who checks the result?

Manual testing

`add.py`

```python
def add(a, b):
    return a + bresult = add(2, 3)
    print(result)  # 5
```

The program displays the result, but it does not check whether the result is correct. You must verify it yourself.

Automated testing

`test_add.py`

```python
def test_add():
    assert add(2, 3) == 5
```

The `assert` statement checks whether the condition is true.

- If `add(2, 3)` returns `5`, the assertion passes.
- If it returns anything else, the assertion fails and raises an `AssertionError`.

When using pytest, a passing test is reported as `PASSED`, while a failing test is reported as `FAILED`.

Key definition: An automated test is code that checks whether other code behaves as expected, without requiring you to verify the result manually each time.

## Why do we need automated tests?

### 100 functions, one change

Imagine an application with 100 functions that depend on one another. You modify one function to add a new feature, but that change unintentionally affects other parts of the application.

The application might still run, even though some features are now broken. Without automated tests, you may not notice the problem until someone encounters it.

Manually checking every feature takes time and makes it easy to overlook errors. Automated tests can run these checks repeatedly and identify unexpected behavior.

Automated tests help you:

- Detect errors: Identify when code produces unexpected results.
- Save time: Run checks automatically instead of repeating them manually.
- Prevent regressions: Catch situations where a new change breaks functionality that previously worked.
- Make changes with confidence: Verify that existing behavior still works after modifying the code.

Key definition: Automated tests help verify that code works as expected and continues to work after changes are made.

---

## What is pytest?

`pytest` is a Python testing framework that makes it easy to write, run, and manage automated tests. It provides a simple syntax for checking results, identifies failing tests, and displays useful information to help you understand what went wrong.

### The same test, two ways to write it

Both examples check whether the string `"1.9"` is less than `"1.10"` using Python's string comparison rules.

1\. `unittest` — included with Python

File: `test_check.py`

```python
import unittest

class TestVersion(unittest.TestCase):    
def test_version(self):        
    self.assertLess("1.9", "1.10")
```

`unittest` uses classes that inherit from `unittest.TestCase`. Its assertion methods, such as `assertLess()`, check conditions and report failures.

2\. `pytest` — a popular Python testing framework

File: `test_check.py`

```python
def test_version():
    assert "1.9" < "1.10"
```

`pytest` allows you to write tests using regular Python functions and the built-in `assert` statement. It automatically provides detailed information when an assertion fails.

Both examples pass because Python compares strings lexicographically, character by character. Since `"9"` is greater than `"1"`, `"1.9"` is greater than `"1.10"` under string comparison, so both tests actually fail. To compare version numbers correctly, use a version-parsing library instead of comparing strings directly.

Key definition: `pytest` is a Python testing framework that simplifies writing and running automated tests. It also supports tests written with `unittest`, allowing you to run them without rewriting them.

## Installation

Install `pytest` as a development dependency using `uv`:

```bash
uv add --dev pytest
```

This command adds `pytest` to the project's development dependencies, making it available for testing without treating it as a runtime dependency of the application.

Run your tests with:

```bash
uv run pytest
```

Key definition: A development dependency is a package needed to develop, test, or maintain a project but not necessarily required to run the application in production.

## Configuration

`pytest` can be configured through `pyproject.toml`, a standard Python project configuration file.

Configuration lets you define how pytest discovers tests and which settings it uses when running them.

Example:

```toml
[tool.pytest.ini_options]
minversion = "9.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
pythonpath = ["."]
```

Note: The correct configuration section for pytest in `pyproject.toml` is `[tool.pytest.ini_options]`, not `[tool.pytest]`. Also, `pytest` 9.0 or later is required if you specify `minversion = "9.0"`.

### What each setting means

- `minversion = "9.0"`: Requires pytest version 9.0 or newer to run the test suite.
- `testpaths = ["tests"]`: Tells pytest to look for tests in the `tests` directory by default.
- `python_files = ["test_*.py"]`: Identifies Python files whose names start with `test_` as potential test files.
- `python_functions = ["test_*"]`: Identifies functions whose names start with `test_` as test functions.
- `pythonpath = ["."]`: Adds the project root directory to Python's import path, helping tests import modules from the project.

Key definition: Pytest configuration defines the rules pytest follows when discovering and running tests, helping keep testing consistent across a project.

---

## Discovery

### How pytest finds tests

Pytest automatically discovers tests by following naming conventions and configuration settings. You usually don't need to specify each test individually.

- `uv run pytest`: Runs pytest, which searches for and executes tests automatically.
- Test directories: Pytest searches the directories specified by `testpaths` in `pyproject.toml`. If `testpaths` is not configured, it generally starts searching from the current directory.
- Test files: By default, pytest looks for files named `test_*.py` or `*_test.py`. You can customize these patterns using `python_files`.
- Test functions and methods: Pytest identifies functions whose names match `python_functions`, which defaults to `test_*`. It also discovers test methods inside classes named `Test*`, provided those classes do not define an `__init__` method.
- Test results: Pytest reports how many tests passed, failed, were skipped, or were not executed for other reasons.

Example: If pytest reports `1 passed, 2 deselected`, one test passed and two were deliberately excluded from execution. If only one test was discovered, the other two might not match the discovery rules at all.

Just because all discovered tests pass does not mean every test you intended to run was discovered or executed.

Run pytest in verbose mode to see the name and result of each executed test:

```bash
uv run pytest -v
```

Key definition: Test discovery is the process by which pytest automatically identifies test files, functions, and methods based on naming conventions and configuration settings.

## Anatomy of a test

### Name, data, and assertion

A test commonly has three main parts:

1. Name: Describes the behavior being tested.
2. Data: Provides the objects or values needed for the test.
3. Assertion: Checks whether the actual behavior matches the expected result.

File: `tests/test_inventory.py`

```python
from inventory import Server


def test_older_version_is_lower():
    old = Server("etl-01", "ubuntu", "20.04")
    new = Server("web-02", "ubuntu", "24.04")

    assert old < new
```

### 1. Test function name

```python
def test_older_version_is_lower():
```

The `test_` prefix allows pytest to recognize the function as a test.

The name describes the behavior we want to verify: that the older server version is considered lower than the newer one.

Descriptive test names make it easier to understand what a test checks when it passes or fails.

### 2. Preparing the data

```python
old = Server("etl-01", "ubuntu", "20.04")
new = Server("web-02", "ubuntu", "24.04")
```

These statements create two `Server` objects with different names and Ubuntu version strings.

The objects provide the data needed to test the comparison behavior. The test assumes that the `Server` class knows how to compare two instances.

### 3. Verification with `assert`

```python
assert old < new
```

`assert` is a built-in Python statement that checks whether an expression evaluates to `True`.

- If the expression is `True`: Execution continues without raising an exception.
- If the expression is `False`: Python raises an `AssertionError`.

For `old < new` to work as intended, the `Server` class must implement appropriate comparison behavior, typically through the `__lt__()` method.

```python
def __lt__(self, other): ...
```

The `__lt__()` method defines how Python evaluates the less-than operator (`<`) for instances of that class.

One important detail: because the server versions are strings, the implementation should compare them as versions rather than relying on ordinary string ordering. Otherwise, some version numbers may be ordered incorrectly.

## What does pytest do with the test?

Pytest executes the test function and determines its outcome based on how the function finishes.

- Passed: The function completes without raising an exception.
- Failed — assertion: An `assert` statement evaluates to `False`, raising an `AssertionError`.
- Failed — unexpected exception: The function raises another unexpected exception, such as `TypeError` or `AttributeError`.

For example, if `Server` does not support comparison with `<`, the test may raise a `TypeError`. Pytest reports the test as failed even though the failure did not come from an `assert` statement.

Key definition: A test passes when its execution completes without an unhandled exception. It fails when an assertion fails or another unexpected exception interrupts its execution.