# Pytest Deep Dive & Fundamentals

This module explores the inner mechanics of **Pytest** and why it is the industry standard for Python testing over traditional `unittest`.

## Core Pillars of Pytest

1. **Plain Assertions**: No need for `self.assertEqual()` or `self.assertTrue()`. Pytest leverages native Python `assert` expressions and performs rich introspection under the hood.
2. **Fixtures (`@pytest.fixture`)**: Reusable setup/teardown components injected cleanly into test functions via dependency injection.
3. **Parametrization (`@pytest.mark.parametrize`)**: Eliminates code duplication by running a single test logic against multiple datasets.
4. **Exception Testing (`pytest.raises`)**: Captures and validates expected errors and boundary limits safely.
