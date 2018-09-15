import unittest

from recread.dynamodb.core import save_gcv_response

class TestBasic(unittest.TestCase):
  def test_can_save(self):
    gcv_response = dict(hei='per')
    image_hash = '123abc'
    actual = save_gcv_response(gcv_response, image_hash)