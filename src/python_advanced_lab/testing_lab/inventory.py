"""
    Module containing inventory structures for infrastructure server nodes.
"""

from typing import Any

class Server:
    """
        Represents an infrastructure server node with capability metrics.
    """

    def __init__(self, name, os, version, services):

        self.name = name
        self.os = os
        self.version = version
        self.services = services

    def __repr__(self):
        return (f"Server({self.name}, {self.os}, {self.version}, {len(self.services)} services)")

    def __eq__(self, other):
        if not isinstance(other, Server):
            return NotImplemented
        return self.name == other.name

    def _version(self):
        return tuple(int(part) for part in self.version.split("."))

    def __lt__(self, other):
        if not isinstance(other, Server):
            return NotImplemented
        # This works only i while commenting out the following line, bc it's comparing the version 
        # numbers as tuples of integers, which is a valid comparison in Python
        return self._version() < other._version()

        # This is the version that will trigger the error.
        # return self._version < other.version

    def __len__(self):
        return len(self.services)