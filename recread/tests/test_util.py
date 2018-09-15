import unittest

from recread.util import hash_bytes

class TestUtil(unittest.TestCase):
  def test_hash_bytes(self):
    byte_string = b''
    actual = hash_bytes(byte_string)
    self.assertIsInstance(actual, str)
