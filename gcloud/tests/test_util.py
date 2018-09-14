import unittest

from gcloud.util import generate_file_name

class TestUtil(unittest.TestCase):
  def test_generate_file_name(self):
    image_bytes = b'an image as bytes'
    actual = generate_file_name(image_bytes)
    self.assertIsInstance(actual, str)
    self.assertGreater(len(actual), 0)
  