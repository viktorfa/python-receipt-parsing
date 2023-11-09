import os
import json
from unittest.mock import MagicMock

from google.cloud import vision
from google.cloud import storage
from recread import config


def get_vision_client_mock():
    with open(
        os.path.join(
            os.path.dirname(__file__), "resources", "kvittering-keiser.jpg.json"
        )
    ) as json_file:
        ocr_response = json.load(json_file)
    mock = MagicMock(vision.ImageAnnotatorClient)
    mock.document_text_detection.return_value = ocr_response
    return mock


def get_storage_client_mock():
    return MagicMock(storage.Client)
