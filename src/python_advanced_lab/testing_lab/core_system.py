"""
    Core system handling infrastructure deployment validations and safety gates.
"""

from typing import NamedTuple


class Version(NamedTuple):
    """
        Structured version tuple for robust mathematical comparisons.
    """
    major: int
    minor: int


class DeploymentGate:
    """
        Validates if a target system is suitable for software deployments.
    """

    def __init__(self, min_version_required: str) -> None:
        self.min_version: Version = self._parse_version(min_version_required)

    def _parse_version(self, version_str: str) -> Version:
        """
            Parses a version string into a safe numeric tuple structure.
        """
        if not version_str or not any(char.isdigit() for char in version_str):
            raise ValueError(f"Invalid version format provided: {version_str!r}")
            
        try:
            parts = [int(p) for p in version_str.split(".")]
            return Version(major=parts[0], minor=parts[1])
        except (ValueError, IndexError) as error:
            raise ValueError(f"Version must follow 'major.minor' numeric format: {version_str!r}") from error

    def is_eligible(self, current_version_str: str) -> bool:
        """
            Checks if the system version satisfies the minimum constraints.
        """
        current_version = self._parse_version(current_version_str)
        # Robust tuple comparison instead of buggy string comparison
        return current_version >= self.min_version
