"""
    Unit tests demonstrating Pytest Data Parametrization techniques.
"""

import pytest
from python_advanced_lab.testing_lab.core_system import DeploymentGate


@pytest.mark.parametrize(
    "current_version, expected_result",
    [
        ("1.10", True),   # Scenario 1: Higher minor version
        ("2.0", True),    # Scenario 2: Higher major version
        ("1.9", True),    # Scenario 3: Exact boundary limit
        ("1.8", False),   # Scenario 4: Lower minor version
        ("0.9", False),   # Scenario 5: Lower major version
    ],
)
def test_gate_eligibility_across_multiple_versions(
    current_version: str, expected_result: bool
) -> None:
    """
        Evaluates multiple boundary version matrix conditions inside a single test loop.
    """
    # Given
    gate = DeploymentGate(min_version_required="1.9")
    
    # When & Then
    assert gate.is_eligible(current_version) is expected_result
