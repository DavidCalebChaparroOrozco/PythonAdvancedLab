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


## Structuring tests, expected errors, and reading results

## Given-When-Then (Arrange, Act, and Assert)

A testing structure that divides a test into three parts to make it easier to understand: the initial conditions, the action performed, and the expected result.

### GIVEN — Arrange

Defines the initial conditions of the test. This includes creating the objects, setting up the data, and preparing everything needed for the test.

### WHEN — Act

Defines the action being tested. This is what the user or system does during the test.

### THEN — Assert

Defines the expected result and verifies that the actual result matches it.

### Example: Testing the Number of Services on a Server

The `test_len` example contains three main components:

- `Server("etl-01", ...)`: Creates a server object with its initial data.
- `len(server)`: Gets the number of services associated with the server.
- `assert cantidad == 2`: Verifies that the server has two services.

We can organize these components into the Given-When-Then structure and give the test a descriptive name.

```python
def test_server_returns_number_of_services():
    # Given: a server with two services
    server = Server(
        "etl-01", "ubuntu", "20.04", ["airflow", "dbt"]
    )

    # When: we get the number of services
    count = len(server)

    # Then: the server has two services
    assert count == 2
```

- Given: Create a server with two services: `airflow` and `dbt`.
- When: Get the number of services using `len(server)` and store the result in `cantidad`.
- Then: Verify that `cantidad` equals `2`.

The test passes if the server reports exactly two services. Otherwise, it fails.

The test name, `test_server_returns_number_of_services`, describes what the test verifies.

## When the Action Changes the State

Some actions modify an object's state. In these cases, the Given-When-Then structure helps us verify that the object changes as expected after the action is performed.

- Given: Establish the initial state of the object.
- When: Perform an action that changes the object's state.
- Then: Verify that the object is in the expected state after the action.

### Example: Testing Service Installation

```python
def test_install_adds_a_service():
    # Given: a server with two services
    server = Server(
        "etl-01", "ubuntu", "20.04", ["airflow", "dbt"]
    )

    # When: we install an additional service
    server.install("grafana")

    # Then: the server has three services
    assert len(server) == 3
```

- Given: Create a server that has two services: `airflow` and `dbt`.
- When: Install an additional service called `grafana`.
- Then: Verify that the server now has three services.

The test passes if installing `grafana` increases the number of services from two to three.

Key difference between the two examples: In the first test, the action retrieves information without intentionally changing the server's state. In the second test, the action modifies the server's state by adding a service, and the test verifies the resulting change.


---

## What If the Action Is a Comparison?

When the action being tested is a comparison, we can store its result in a variable, such as `resultado`. This makes the When step (the action) separate from the Then step (the verification), making the test easier to read and understand.

```python
def test_older_version_is_lower():
    # Given: two servers with different versions
    old = Server(
        "etl-01", "ubuntu", "18.04", ["airflow"]
    )
    new = Server(
        "web-01", "ubuntu", "24.04", ["nginx"]
    )

    # When: we compare both servers
    resultado = old < new

    # Then: the older server is considered lower
    assert resultado
```

- Given: Create two servers with different Ubuntu versions: one running `18.04` and the other running `24.04`.
- When: Compare the two servers using the `<` operator and store the result in `resultado`.
- Then: Verify that the comparison returns `True`, meaning that `old` is considered less than `new`.

This test assumes that the `Server` class implements the `<` operator so that servers are compared according to their Ubuntu versions.

> Note: Writing `assert old < new` is also perfectly valid. Storing the comparison in a variable is optional; it is useful when separating the action from the verification makes the test clearer or easier to understand.

---

## The Test Name Also Communicates

A test name should describe the behavior being verified, not just the method or operation being executed. A good name makes it clear what the test checks and what outcome is expected.

| Not very descriptive | Describes the behavior                             |
| -------------------- | -------------------------------------------------- |
| `test_len()`         | `test_server_returns_number_of_services()`         |
| `test_install()`     | `test_install_adds_a_service()`                    |
| `test_lt()`          | `test_older_version_is_lesser()`                   |
| `test_error()`       | `test_installing_duplicate_service_raises_error()` |

The first column uses vague names that tell us little about what the test verifies. The second column uses descriptive names that explain the expected behavior.

For example, `test_install()` tells us that the test involves installing something, but it does not explain what should happen. In contrast, `test_install_adds_a_service()` clearly states the expected behavior: installing a service should add it to the server.

## Why Does the Test Name Matter So Much?

When a test fails, its name is one of the first things we see in the test report. A descriptive name helps us quickly understand what behavior failed, even before examining the test code.

For example, when running tests with `uv run pytest`, the terminal might display a failure such as:

```
FAILED test_server.py::test_installing_duplicate_service_raises_error
```

From this line alone, we can tell that the test for installing a duplicate service did not behave as expected. We can then investigate the code to determine why.

A clear test name makes failures easier to identify, understand, and debug, especially when a project contains many tests.

---

## Testing Expected Errors

Sometimes, the correct behavior of a program is to reject an operation and raise an exception. This can happen when a user tries to perform an invalid action, such as installing a service that is already installed.

We should test these situations just as we test successful operations. The goal is to verify that the code raises the expected type of exception when an invalid operation occurs.

```python
class Server:
    ...

    def install(self, service: str) -> None:
        """
        Installs an additional service in the environment.
        """
        if service in self.services:
            raise ValueError("The service is already installed")

        self.services.append(service) self.services.append(service)
```

In this example, the `install()` method checks whether the service is already installed. If it is, the method raises a `ValueError` instead of adding the service again. Otherwise, it adds the service to the list.

## `pytest.raises`: Verifying That an Error Occurs as Expected

`pytest.raises()` allows us to test whether a specific exception is raised when a piece of code runs.

The test passes if the code raises the specified exception or one of its subclasses. It fails if no exception is raised or if an exception of an incompatible type is raised.

```python
import pytest

def test_installing_duplicate_service_raises_error():
    # Given: a server that already has 'dbt' installed
    server = Server(
        "etl-01", "ubuntu", "20.04", ["airflow", "dbt"]
    )

    # When / Then: installing 'dbt' should raise a ValueError
    with pytest.raises(ValueError):
        server.install("dbt")
```

- Given: Create a server that already has `dbt` installed.
- When: Attempt to install `dbt` again.
- Then: Verify that the operation raises a `ValueError`.

The test passes because the `install()` method raises the expected exception when it encounters a duplicate service.

Important: The exception type in the test must match the exception the code is expected to raise. In this example, the correct type is `ValueError`, not `TypeError`.

> We don't just check that the code fails; we check that it fails in the expected way.

With `pytest.raises()`, the When and Then steps are combined because the action is performed inside the context manager, and the context manager verifies the exception.

Exception subclasses also count. For example, `UnicodeDecodeError` is a subclass of `ValueError`, so it would satisfy `pytest.raises(ValueError)`.

## Also Checking the Error Message: `match` and `as error`

Sometimes, checking the exception type is not enough. We may also want to verify that the exception contains the expected message.

There are two common ways to do this with `pytest.raises()`.

### `match`: Checking the Error Message

The `match` argument lets us verify that the exception message contains a pattern we expect.

```python
with pytest.raises(ValueError, match="The service is already installed"):
    server.install("dbt")
```

In this example, the test verifies two things:

- The operation raises a `ValueError`.
- The exception message matches the specified pattern.

A `ValueError` can be raised for many different reasons. Checking the message helps us confirm that the error occurred for the expected reason.

How does `match` work?

The `match` argument uses a regular expression (regex) to search the exception message with `re.search()`. The pattern does not need to match the entire message; it only needs to match part of it.

Certain characters, such as `.`, `*`, `(`, and `)`, have special meanings in regular expressions. If you want to match a message containing these characters literally, use `re.escape()`.

For example:

```python
import re
import pytest

expected_message = "Invalid service (dbt)"

with pytest.raises(ValueError, match=re.escape(expected_message)):
    server.install("dbt")
```

Use `re.escape()` when the expected message contains characters that could otherwise be interpreted as regex syntax.

### `as error`: Capturing the Exception

The `as error` syntax lets us capture the exception object so we can inspect it after the code inside the `with` block executes.

```python
with pytest.raises(ValueError) as error:
    server.install("dbt")

assert "The service is already installed" in str(error.value)
```

Here's how it works:

- `pytest.raises(ValueError)` verifies that a `ValueError` is raised.
- `as error` stores information about the captured exception in the `error` variable.
- `error.value` gives us the actual exception object.
- `str(error.value)` converts the exception to a string, allowing us to inspect its message.
- `assert` checks that the expected text appears in that message.

The test fails if the expected exception is not raised or if the message does not contain the specified text.

Key difference:

- Use `match` when you want to verify the exception message directly within `pytest.raises()`.
- Use `as error` when you need to access the exception object, inspect its message with an assertion, or perform additional checks on the exception.

Both approaches let you verify not only that an error occurs, but also that it is the correct error for the situation being tested.

---


## Running Only the Tests You Need

When a project contains many tests, you don't always need to run all of them. With `pytest`, you can choose which tests to execute based on the file they belong to, a keyword in their names, or their exact test name.

| Method                         | Command                                                                | What it does                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| By file                        | `uv run pytest tests/test_inventory.py`                                | Runs all tests in the specified file.                                                                    |
| By keyword                     | `uv run pytest -k install -v`                                          | Runs tests whose names or file paths contain `install`. The `-v` flag displays more detailed output.     |
| Exclude by keyword             | `uv run pytest -k "not message"`                                       | Runs tests that do not match `message` in their names or file paths.                                     |
| By exact test name (node ID)   | `uv run pytest "tests/test_inventory.py::test_install_adds_a_service"` | Runs only the specified test.                                                                            |
| Be careful with broad keywords | `uv run pytest -k inventory`                                           | Runs every test whose name or file path matches `inventory`, which may include more tests than intended. |

### Understanding the Commands

1\. Run tests by file

Use the file path when you want to run all tests defined in a particular file.

```bash
uv run pytest tests/test_inventory.py
```

2\. Run tests by keyword

Use `-k` to select tests whose names or file paths contain a particular term.

```bash
uv run pytest -k install -v
```

This runs matching tests and displays their names and results in more detail.

3\. Exclude tests using `not`

You can use `not` to exclude tests that match a keyword.

```bash
uv run pytest -k "not message"
```

This runs tests that do not match `message`. Remember that the keyword is matched against both test names and file paths, so the results may include or exclude tests based on either.

4\. Run a specific test using its node ID

A node ID identifies a particular test by its file path and test name, separated by `::`.

```bash
uv run pytest "tests/test_inventory.py::test_install_adds_a_service"
```

This runs only the specified test function.

5\. Be careful with broad keywords

```bash
uv run pytest -k inventory
```

This may run tests from multiple files if their names or paths contain `inventory`. Before using a broad keyword, consider whether it matches more tests than you intended.

> Important: The `-k` flag performs a case-insensitive match against test names and their parent names, including file and directory names. You can combine expressions using operators such as `and`, `or`, and `not`.

Use double quotes around expressions such as `-k "not message"` to make the command work consistently in both PowerShell and Bash.