import unittest
from unittest.mock import patch

from gcloud.ocr import get_vision_client

class TestOcr(unittest.TestCase):
  @patch('google.cloud.vision.ImageAnnotatorClient')
  def test_basic(self, mock_vision_client):
    actual = get_vision_client()
    self.assertIsNotNone(actual)
    self.assertTrue(mock_vision_client.called_once)