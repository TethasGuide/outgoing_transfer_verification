import logging
from unittest.mock import patch, MagicMock

from verification_function import fetch_weight_for_tag


def test_fetch_weight_for_tag_success():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"weight": 5, "weight_unit": "g"}]
    with patch("verification_function.requests.get", return_value=mock_resp) as mock_get:
        logger = logging.getLogger("test")
        weight, unit = fetch_weight_for_tag("TAG1", logger)
    mock_get.assert_called_once()
    assert weight == 5
    assert unit == "g"


def test_fetch_weight_for_tag_empty_response(caplog):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = []
    with patch("verification_function.requests.get", return_value=mock_resp):
        logger = logging.getLogger("test")
        with caplog.at_level(logging.WARNING):
            weight, unit = fetch_weight_for_tag("TAG123", logger)
    assert weight == 0
    assert unit is None
    assert "No data returned for tag TAG123" in caplog.text


def test_fetch_weight_for_tag_error(caplog):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.text = "not found"
    with patch("verification_function.requests.get", return_value=mock_resp):
        logger = logging.getLogger("test")
        with caplog.at_level(logging.ERROR):
            weight, unit = fetch_weight_for_tag("TAG404", logger)
    assert weight == 0
    assert unit is None
    assert "Error fetching weight for tag TAG404" in caplog.text
