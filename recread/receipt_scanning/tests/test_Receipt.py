import unittest
import json

from recread.receipt_scanning.Receipt import Receipt, ReceiptLine
from recread.receipt_scanning import lib

with open('./data/receipt_responses/kvittering-keiser-2.jpg.json') as keiser_json_file:
  keiser_json_object = json.load(keiser_json_file)

class Test_Receipt(unittest.TestCase):
  def test_can_instantiate(self):
    actual = lib.read_receipt_from_google_ocr_json(keiser_json_object)
    self.assertIsInstance(actual, Receipt)

  def test_has_token_lines(self):
    actual = lib.read_receipt_from_google_ocr_json(keiser_json_object)
    self.assertIsInstance(actual.token_lines, list)
    self.assertGreater(len(actual.token_lines), 0)

  def test_can_get_products(self):
    receipt = lib.read_receipt_from_google_ocr_json(keiser_json_object)
    actual = receipt.get_all_products()
    self.assertIsInstance(actual, list)
    self.assertGreater(len(actual), 0)
    print('PRODUCTS')
    for product in actual:
      print(product)


class TestReceiptLine(unittest.TestCase):
  def test_can_parse_price(self):
    actual = ReceiptLine(['1', 'Hvitlok', '500g', '12,90'])
    self.assertEqual(actual.prices[0]['value'], 12.90)
  
  def test_can_parse_weight(self):
    actual = ReceiptLine(['1,008', 'kg', 'X', '12,90/kg'])
    self.assertEqual(actual.weights[0]['value'], 1.008)
    self.assertEqual(actual.weights[0]['unit'], 'kg')

  def test_can_parse_unit_price(self):
    actual = ReceiptLine(['0,338', 'kg', 'X', '49,90/kg'])
    self.assertEqual(actual.unit_prices[0]['value'], 49.90)
    self.assertEqual(actual.unit_prices[0]['unit'], 'kg')