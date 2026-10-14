"""
    Unit tests to practice Pytest discovery, introspection, and assertions.
"""

from python_advanced_lab.testing_lab.core_system import DeploymentGate
import pytest

def test_system_version_satisfies_minimum_gate_requirement() -> None:
    """
        Verifies that a newer or equal system version successfully passes the gate.
    """
    # 1. Preparing the data
    gate = DeploymentGate(min_version_required="1.9")
    
    # 2. Executing & Asserting (The native 'assert' statement checks the truth value)
    assert gate.is_eligible("1.10") is True


def test_system_version_fails_under_minimum_gate_requirement() -> None:
    """
        Verifies that an older system version is correctly rejected by the gate.
    """
    # 1. Preparing the data
    gate = DeploymentGate(min_version_required="1.9")
    
    # 2. Executing & Asserting
    assert gate.is_eligible("1.8") is False

def test_gate_raises_value_error_on_non_numeric_version() -> None:
    """
        Verifies the gate crashes safely when a corrupted version string is evaluated.
    """
    # Given
    gate = DeploymentGate(min_version_required="1.9")
    
    # When & Then (Using the context manager to catch the expected error)
    with pytest.raises(ValueError) as exc_info:
        gate.is_eligible("invalid_version_string")
        
    # Introspection: You can inspect the exact error message inside the exception
    assert "Invalid version format provided" in str(exc_info.value)


def test_gate_raises_value_error_on_malformed_format() -> None:
    """
        Verifies rejection when the version string does not meet major.minor formatting.
    """
    with pytest.raises(ValueError, match="Version must follow 'major.minor'"):
        DeploymentGate(min_version_required="2")