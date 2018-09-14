import unittest
from unittest.mock import MagicMock

from google.cloud import storage

from gcloud.storage import store_image_in_gcloud

class TestStorage(unittest.TestCase):
  def setUp(self):
    self.storage_client_mock = MagicMock(storage.Client)

  def test_basic(self):
    image_bytes = b'a byte string'
    actual = store_image_in_gcloud(image_bytes, self.storage_client_mock)
    self.assertIsInstance(actual, str)
    self.storage_client_mock.assert_called_once
    