"""
    Module containing inventory structures for infrastructure server nodes.
"""

from typing import Any

class Server:
    """
        Represents an infrastructure server node with capability metrics.
    """

    def __init__(self, name:str , os_name: str, version: str, services: list[str]) -> None:

        self.name: str = name
        self.os: str = os_name
        self.version: str = version
        self.services: list[str] = list(services)

    def __repr__(self) -> str:
                return f"Server({self.name}, {self.os}, {self.version}, {len(self.services)} services)"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        return self.name == other.name

    def _version(self) -> tuple[int, ...]:
        return tuple(int(part) for part in self.version.split("."))

    def __lt__(self, other: "Server") -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        # This works only i while commenting out the following line, bc it's comparing the version 
        # numbers as tuples of integers, which is a valid comparison in Python
        return self._version() < other._version()

        # This is the version that will trigger the error.
        # return self._version < other.version

    def __len__(self) -> int:
        return len(self.services)