"""
Module to practice Python Data Model initialization and representation protocols.
"""

from typing import Self


class AdvancedDeveloper:
    """
        Represents a developer with core metrics using Python Data Model techniques.
    """

    def __init__(self, username: str, experience_years: int, skills: list[str]) -> None:
        self.username: str = username
        self.experience_years: int = experience_years
        self.skills: list[str] = list(skills)  # Create a copy to prevent mutation bugs

    def __repr__(self) -> str:
        """
        Unambiguous representation for developers.

        Should look like valid Python code to recreate the object.
        """
        return (
            f"{self.__class__.__name__}("
            f"username={self.username!r}, "
            f"experience_years={self.experience_years!r}, "
            f"skills={self.skills!r})"
        )

    def __str__(self) -> str:
        """
        User-friendly representation for logging and display purposes.
        """
        return f"Developer @{self.username} ({self.experience_years} YOE) | Skills: {', '.join(self.skills)}"

    def add_skill(self, skill: str) -> Self:
        """
        Adds a new skill and returns the instance fluently using PEP 673 Self.
        """
        clean_skill = skill.strip().title()
        if clean_skill not in self.skills:
            self.skills.append(clean_skill)
        return self
