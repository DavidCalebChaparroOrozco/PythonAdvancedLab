"""
Module practicing multiple 'for' clauses in comprehensions and typed arrays.
"""

from array import array

from python_advanced_lab.testing_lab.inventory import Server


def get_sample_fleet() -> tuple[list[Server], tuple[str, ...], array[int]]:
    """
    Provides the baseline infrastructure dataset for sequence transformations.
    """
    servers: list[Server] = [
        Server("etl-01", "ubuntu", "22.04", ["airflow", "dbt"]),
        Server("db-01", "debian", "12.5", ["postgres"]),
        Server("web-01", "ubuntu", "20.04", ["nginx", "gunicorn", "redis"]),
        Server("bi-01", "rocky", "9.3", []),
    ]
    checks: tuple[str, ...] = ("cpu", "disk", "memory")
    ports: array[int] = array("H", [22, 80, 443, 5432, 8080])
    return servers, checks, ports


def generate_health_check_matrix(
    servers: list[Server], checks: tuple[str, ...]
) -> list[tuple[str, str]]:
    """
    Cartesian product: pairs every server name with every health check.
    """
    return [(server.name, check) for server in servers for check in checks]


def flatten_installed_services(servers: list[Server]) -> list[str]:
    """
    Flattening nested lists: extracts all installed services across the fleet.
    """
    return [service for server in servers for service in server.services]


def get_ubuntu_services(servers: list[Server]) -> list[str]:
    """
    Nested comprehension with filtering: services running only on Ubuntu nodes.
    """
    return [service for server in servers if server.os == "ubuntu" for service in server.services]


def format_port_bindings(
    servers: list[Server], ports: array[int], target_os: str = "ubuntu"
) -> list[str]:
    """
    Combines container sequences with a flat typed array ('H') for endpoint mapping.
    """
    return [
        f"{server.name}:{port}" for server in servers if server.os == target_os for port in ports
    ]
