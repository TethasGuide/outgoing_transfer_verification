import logging
from unittest.mock import patch, MagicMock

import os
import sys
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if 'requests' not in sys.modules:
    requests_stub = ModuleType('requests')
    requests_stub.get = lambda *args, **kwargs: None
    sys.modules['requests'] = requests_stub

if 'office365' not in sys.modules:
    office365 = ModuleType('office365')
    runtime = ModuleType('runtime')
    auth_mod = ModuleType('auth')
    user_cred_mod = ModuleType('user_credential')
    user_cred_mod.UserCredential = type('UserCredential', (), {})
    auth_mod.user_credential = user_cred_mod
    runtime.auth = auth_mod
    sharepoint_mod = ModuleType('sharepoint')
    client_ctx_mod = ModuleType('client_context')
    client_ctx_mod.ClientContext = type('ClientContext', (), {})
    sharepoint_mod.client_context = client_ctx_mod
    office365.runtime = runtime
    office365.sharepoint = sharepoint_mod
    sys.modules['office365'] = office365
    sys.modules['office365.runtime'] = runtime
    sys.modules['office365.runtime.auth'] = auth_mod
    sys.modules['office365.runtime.auth.user_credential'] = user_cred_mod
    sys.modules['office365.sharepoint'] = sharepoint_mod
    sys.modules['office365.sharepoint.client_context'] = client_ctx_mod

from verification_function import fetch_weight_for_tag


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
