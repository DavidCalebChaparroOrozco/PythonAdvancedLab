"""
    Unit tests for the Server comparison protocols (Data Model).
"""

from python_advanced_lab.data_model.operators import Server


def test_server_equality_by_name() -> None:
    """
    Ensures servers with the same name are considered equal.
    """
    a = Server("web-01", "ubuntu", "22.04")
    b = Server("web-01", "debian", "11.0")
    assert a == b


def test_server_version_comparison() -> None:
    """
    Validates that older versions are correctly identified via __lt__.
    """
    older = Server("db-01", "ubuntu", "20.10")
    newer = Server("db-02", "ubuntu", "22.04")
    
    assert older < newer
    assert not newer < older
    assert min([newer, older]) == older
