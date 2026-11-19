from unittest.mock import MagicMock, patch

from python_advanced_lab.sequences_lab.queries import is_port_open


@patch("socket.create_connection")
def test_is_port_open_returns_true_when_connection_succeeds(mock_connect: MagicMock) -> None:
    # Given: A host and port that successfully accept a TCP connection
    host = "db-01"
    port = 5432

    # When: We check if the port is open
    result = is_port_open(host, port)

    # Then: True is returned and create_connection was invoked with expected arguments
    assert result is True
    mock_connect.assert_called_once_with((host, port), timeout=1.0)


@patch("socket.create_connection", side_effect=OSError("Connection refused"))
def test_is_port_open_returns_false_when_connection_fails(mock_connect: MagicMock) -> None:
    # Given: A host and port that refuse or time out the TCP connection
    host = "bi-01"
    port = 5432

    # When: We check if the port is open
    result = is_port_open(host, port)

    # Then: False is returned safely without crashing
    assert result is False
