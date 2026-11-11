"""
Unit tests for multiple 'for' clauses in comprehensions and typed arrays.
"""

from python_advanced_lab.sequences_lab.transformations import (
    flatten_installed_services,
    format_port_bindings,
    generate_health_check_matrix,
    get_sample_fleet,
    get_ubuntu_services,
)


def test_generate_health_check_matrix_produces_cartesian_product() -> None:
    # Given: A fleet of 4 servers and 3 health checks
    servers, checks, _ = get_sample_fleet()

    # When: We generate the health check matrix
    matrix = generate_health_check_matrix(servers, checks)

    # Then: All 12 combinations (4 x 3) are created in outer-to-inner order
    assert len(matrix) == 12
    assert matrix[0] == ("etl-01", "cpu")
    assert matrix[1] == ("etl-01", "disk")
    assert matrix[-1] == ("bi-01", "memory")


def test_flatten_installed_services_extracts_all_services() -> None:
    # Given: Servers with varying numbers of services (including an empty list)
    servers, _, _ = get_sample_fleet()

    # When: We flatten all installed services across the fleet
    services = flatten_installed_services(servers)

    # Then: A single flat list with all 6 services is returned
    assert services == ["airflow", "dbt", "postgres", "nginx", "gunicorn", "redis"]


def test_get_ubuntu_services_filters_by_os() -> None:
    # Given: A mixed-OS server fleet
    servers, _, _ = get_sample_fleet()

    # When: We extract services only from Ubuntu servers
    ubuntu_services = get_ubuntu_services(servers)

    # Then: Only services from etl-01 and web-01 are included
    assert ubuntu_services == ["airflow", "dbt", "nginx", "gunicorn", "redis"]


def test_format_port_bindings_combines_fleet_and_typed_array() -> None:
    # Given: The sample fleet and an unsigned short ('H') array of ports
    servers, _, ports = get_sample_fleet()

    # When: We bind ports for 'debian' servers
    bindings = format_port_bindings(servers, ports, target_os="debian")

    # Then: Only db-01 endpoints are formatted for the 5 ports
    assert bindings == [
        "db-01:22",
        "db-01:80",
        "db-01:443",
        "db-01:5432",
        "db-01:8080",
    ]
