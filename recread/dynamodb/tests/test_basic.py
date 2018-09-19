import unittest
from unittest.mock import patch
from recread.dynamodb.core import save_gcv_response

class TestBasic(unittest.TestCase):
  @patch('recread.dynamodb.core.GcvResponseModel')
  def test_can_save(self, GcvResponseModelMock):
    gcv_response = dict(hei='per')
    image_hash = '123abc'
    actual = save_gcv_response(gcv_response, image_hash)