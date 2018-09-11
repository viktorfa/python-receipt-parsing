import unittest

from gcloud.ocr import store_and_get_ocr_response_from_base64_image_string

class TestOcr(unittest.TestCase):
  def test_basic_test(self):
    base64string = 'cnVtcGEgdGlsIGthYXJl'
    actual = store_and_get_ocr_response_from_base64_image_string(base64string)