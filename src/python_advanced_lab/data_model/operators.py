"""
    Module to practice Python Data Model operator overloading and comparisons.
"""
from typing import Any

class Server:
    """
        Represents a network server with version tracking and comparison protocols.
    """
    def __init__(self, name: str, os_name: str, version: str, services: list[str] | None = None) -> None:
        self.name: str = name
        self.os: str = os_name
        self.version: str = version
        self.services: list[str] = services if services is not None else []

    def __repr__(self) -> str:
        return f"Server({self.name!r}, {self.os} {self.version}, {len(self.services)} svc)"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other:"Server") -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        return self._tuple_version() < other._tuple_version()

    def _tuple_version(self) -> tuple[int, ...]:
        return tuple(int(p) for p in self.version.split("."))  # [22, 04] < [20, 10]


def main() -> None:
    """
        Execution sandbox to reproduce the insights.
    """
    a = Server("web-01", "ubuntu", "22.04", ["nginx", "postgres"])
    b = Server("web-01", "ubuntu", "22.04", ["nginx", "postgres"])  # same data
    c = Server("db-01", "ubuntu", "20.10", ["postgres"])

    print("a:", a)
    print("a == b:", a == b)
    print("a == a:", a == a)
    print("a in [c, b]:", a in [c, b])

    # We are going to add another operation.
    print("a < c:", a < c)

    # Let's assume I want to see the lowest version of the servers.
    servers = [a, b, c]
    print("Lowest version server:", min(servers))

# The first time:
# a: <__main__.Server object at 0x0000019CD2AB0C80>
# a == b: False
# a == a: True
# a in [c, b]: False


# After adding __repr__ and __eq__
# a: Server('web-01', ubuntu 22.04, 2 svc)
# a == b: True
# a == a: True
# a in [c, b]: True


# After adding the "<" operation here, we get an error.
# a: Server('web-01', ubuntu 22.04, 2 svc)
# a == b: True
# a == a: True
# a in [c, b]: True
# Traceback (most recent call last):
#   File "PythonAdvancedLab\src\python_advanced_lab\data_model\__init__.py", line 26, in <module>
#     print("a < c:", a < c)
#                     ^^^^^
# TypeError: '<' not supported between instances of 'Server' and 'Server'


# After creating __lt__ and _tuple_version
# a: Server('web-01', ubuntu 22.04, 2 svc)
# a == b: True
# a == a: True
# a in [c, b]: True
# a < c: False


# Testing with min
# a: Server('web-01', ubuntu 22.04, 2 svc)
# a == b: True
# a == a: True
# a in [c, b]: True
# a < c: False
# Server('db-01', ubuntu 20.10, 1 svc)
# 

if __name__ == "__main__":
    main()