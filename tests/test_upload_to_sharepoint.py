import logging
from unittest.mock import MagicMock, patch, mock_open

import verification_function
from verification_function import TransferApp


def test_upload_uses_configured_library_path():
    app = TransferApp.__new__(TransferApp)
    app.logger = logging.getLogger("test")

    verification_function.SP_MAIN_SITE_URL = "https://example.sharepoint.com"
    verification_function.SP_LIBRARY_PATH = "/sites/doc/lib"

    mock_ctx_instance = MagicMock()
    mock_web = MagicMock()
    mock_ctx_instance.web = mock_web
    mock_web.get_folder_by_server_relative_url.return_value = MagicMock(upload_file=MagicMock())

    with patch("verification_function.ClientContext") as mock_ctx, \
         patch("verification_function.UserCredential"), \
         patch("builtins.open", mock_open(read_data=b"data")):
        mock_ctx.return_value.with_credentials.return_value = mock_ctx_instance
        app.upload_to_sharepoint("local.csv", "remote.csv")

    mock_ctx.assert_called_once_with(
        f"{verification_function.SP_MAIN_SITE_URL}/sites/documentcontrol"
    )
    mock_web.get_folder_by_server_relative_url.assert_called_once_with(
        verification_function.SP_LIBRARY_PATH
    )
