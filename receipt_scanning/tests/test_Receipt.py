import unittest
import json

from receipt_scanning.Receipt import Receipt
from receipt_scanning import lib

with open('./receipt_scanning/tests/data/receipt_keiser.json') as keiser_json_file:
  keiser_json_object = json.load(keiser_json_file)

class Test_Receipt(unittest.TestCase):
  def test_can_instantiate(self):
    actual = lib.read_receipt_from_google_ocr_json(keiser_json_object)
    self.assertIsInstance(actual, Receipt)

  def test_has_token_lines(self):
    actual = lib.read_receipt_from_google_ocr_json(keiser_json_object)
    self.assertIsInstance(actual.token_lines, list)
    self.assertGreater(len(actual.token_lines), 0)
