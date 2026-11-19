"""Module containing inventory queries and server fleet definitions."""

import socket

from python_advanced_lab.testing_lab.inventory import Server

SERVERS: list[Server] = [
    Server("etl-01", "ubuntu", "22.04", ["postgresql", "redis"]),
    Server("db-01", "debian", "12", ["postgresql"]),
    Server("web-01", "ubuntu", "20.04", ["nginx", "redis"]),
    Server("bi-01", "rocky", "9", []),
]


def with_service(servers: list[Server], service: str) -> list[str]:
    """Returns the names of all servers that have the specified service installed."""
    return [server.name for server in servers if service in server.services]


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Returns True if the target host accepts TCP connections on the given port."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


if __name__ == "__main__":
    print(
        "With PostgreSQL: ", with_service(SERVERS, "postgresql")
    )  # With PostgreSQL:  ['etl-01', 'db-01']
    print("With Redis: ", with_service(SERVERS, "redis"))  # With Redis:  ['etl-01', 'web-01']
    print("db-01 accepts TCP on 5432:", is_port_open("db-01", 5432))  # True
    print("bi-01 accepts TCP on 5432:", is_port_open("bi-01", 5432))  # False
