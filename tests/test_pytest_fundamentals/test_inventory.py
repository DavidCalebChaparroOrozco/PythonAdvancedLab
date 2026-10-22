"""
    Unit tests validating the inventory domain entities via pytest assertions.
"""

import pytest
from python_advanced_lab.testing_lab.inventory import Server


def test_older_version_is_lower():
    # Given: two servers with different versions
    old = Server("etl-01", "Ubuntu", "18.04", ["postgresql", "ssh"])
    new = Server("web-02", "Ubuntu", "24.04", ["nginx", "ssh", "cron"])

    # When: we compare both servers
    result = old < new

    # Then: the older server is lower
    assert result


def test_equal_if_they_have_the_same_name():
    # Given: two servers with the same name but different attributes
    a = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])
    b = Server("web001", "Debian", "12.5", ["ssh"])

    # When: we compare both servers for equality
    result = a == b

    # Then: both servers are considered equal
    assert result


def test_length_is_the_number_of_services():
    # Given: a server with three services
    server = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])

    # When: we get the number of services
    count = len(server)

    # Then: the server has three services
    assert count == 3


def test_min_returns_the_most_outdated_one():
    # Given: three servers with difference versions
    a = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])
    b = Server("db001", "Ubuntu", "18.04", ["postgresql", "ssh"])
    d = Server("app001", "Ubuntu", "9.10", ["python"])

    # When: we find the server with the minimum version
    result = min([a, b, d])

    # Then: the server with the oldest version is returned
    assert result is d

def test_install_adds_a_service():
    # Given: a server with two services
    server = Server(
        "etl-01", "ubuntu", "20.04", ["airflow", "dbt"]
    )

    # When: we install an additional service
    server.install("grafana")

    # Then: the server has three services
    assert len(server) == 3

def test_install_duplicate_service_raises_error() -> None:
    # Given: A server that already has dbt
    server = Server("etl-01", "ubuntu", "20.04", ["airflow", "dbt"])

    # When / Then: Installing dbt should raise a ValueError.
    with pytest.raises(ValueError, match="The service is already installed"):
        server.install("dbt")