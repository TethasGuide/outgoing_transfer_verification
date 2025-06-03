import logging
from unittest.mock import patch

from verification_function import TransferApp


def test_process_transfers():
    transfer = {
        "destinations": [
            {
                "contents": [
                    {
                        "package": {
                            "tag": "TAG1",
                            "item": {
                                "name": "Item1",
                                "sub_type": {"name": "SubtypeA"}
                            }
                        }
                    }
                ]
            }
        ]
    }

    app = TransferApp.__new__(TransferApp)
    app.logger = logging.getLogger("test")

    with patch("verification_function.fetch_weight_for_tag", return_value=(10, "kg")):
        result = TransferApp.process_transfers(app, transfer)

    assert result == {
        "TAG1": {
            "item_name": "Item1",
            "sub_type_name": "SubtypeA",
            "weight": 10,
            "weight_unit": "kg",
        }
    }
