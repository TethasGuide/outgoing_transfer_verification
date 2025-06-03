import logging
from unittest.mock import patch, MagicMock

from verification_function import get_transfers


def test_get_transfers_success():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    expected_data = [{"id": 1}]
    mock_resp.json.return_value = expected_data
    with patch("verification_function.requests.get", return_value=mock_resp) as mock_get:
        logger = logging.getLogger("test")
        result = get_transfers("http://example.com/api", {}, logger)
    mock_get.assert_called_once_with("http://example.com/api", headers={})
    assert result == expected_data


def test_get_transfers_failure(caplog):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.text = "server error"
    with patch("verification_function.requests.get", return_value=mock_resp):
        logger = logging.getLogger("test")
        with caplog.at_level(logging.ERROR):
            result = get_transfers("http://bad.api", {}, logger)
    assert result is None
    assert "Error: 500 server error" in caplog.text
