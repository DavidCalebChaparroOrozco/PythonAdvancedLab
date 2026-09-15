"""
Unit tests for the Data Model representation protocol.
"""

from python_advanced_lab.data_model.representation import AdvancedDeveloper


def test_developer_representation_protocols() -> None:
    """
    Validates __repr__ and __str__ produce the exact expected outputs.
    """
    # Given
    dev = AdvancedDeveloper(
        username="caleb_dev", experience_years=5, skills=["Python", "Git"]
    )

    # When & Then (Testing __repr__)
    expected_repr = "AdvancedDeveloper(username='caleb_dev', experience_years=5, skills=['Python', 'Git'])"
    assert repr(dev) == expected_repr

    # When & Then (Testing __str__)
    expected_str = "Developer @caleb_dev (5 YOE) | Skills: Python, Git"
    assert str(dev) == expected_str


def test_fluent_skill_addition() -> None:
    """Validates safe mutation and modern Self type handling."""
    dev = AdvancedDeveloper(username="test_user", experience_years=1, skills=[])

    # Fluent interface test
    updated_dev = dev.add_skill("rust").add_skill("python")

    assert updated_dev is dev
    assert "Rust" in dev.skills
    assert "Python" in dev.skills
