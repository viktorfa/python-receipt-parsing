import unittest
import json
import os

from recread import config
from recread.receipt.core import read_receipt_from_google_ocr_json
from recread.receipt.models import ReceiptProduct

RECEIPT_FILE_NAME_KEISER = 'kvittering-keiser.jpg.json'
RECEIPT_FILE_NAME_KIWI = 'kvittering-kiwi.jpg.json'
RECEIPT_FILE_NAME_IKEA = 'kvittering-ikea.jpg.json'
RECEIPT_FILE_NAME_PRIX = 'kvittering-coop-prix.jpg.json'

with open(os.path.join(config.PROJECT_DIR, 'data', 'receipt_responses', RECEIPT_FILE_NAME_KEISER)) as json_file:
    json_ocr_keiser = json.load(json_file)
with open(os.path.join(config.PROJECT_DIR, 'data', 'receipt_responses', RECEIPT_FILE_NAME_KIWI)) as json_file:
    json_ocr_kiwi = json.load(json_file)
with open(os.path.join(config.PROJECT_DIR, 'data', 'receipt_responses', RECEIPT_FILE_NAME_IKEA)) as json_file:
    json_ocr_ikea = json.load(json_file)
with open(os.path.join(config.PROJECT_DIR, 'data', 'receipt_responses', RECEIPT_FILE_NAME_PRIX)) as json_file:
    json_ocr_prix = json.load(json_file)

class TestE2EParsing(unittest.TestCase):
  def test_keiser_receipt(self):
    receipt = read_receipt_from_google_ocr_json(json_ocr_keiser)
    expected_sum = 123.00
    expected_products = [
      ReceiptProduct('ingefær', 2.63),
      ReceiptProduct('tomater', 14.90),
      ReceiptProduct('lime', 16.87),
      ReceiptProduct('koriander', 12.90),
      ReceiptProduct('løk', 13.00),
      ReceiptProduct('hvitløk', 12.90, quantity=dict(value=500, unit='g')),
      ReceiptProduct('tine helmelk', 17.90),
      ReceiptProduct('agurk', 14.90),
      ReceiptProduct('grønt', 16.90),
    ]

    self.assertEqual(receipt.get_sum(), expected_sum, f'Sum should be {expected_sum}')
    actual_products = receipt.get_all_products()
    self.assertEqual(len(actual_products), len(expected_products), f'Should find {len(expected_products)} products')
    for i, product in enumerate(actual_products):
      self.assertAlmostEqual(product.price, expected_products[i].price, msg=f'price is incorrect for {product}')
      if (expected_products[i].quantity):
        self.assertEqual(expected_products[i].quantity['value'], product.quantity['value'])

  def test_kiwi_receipt(self):
    receipt = read_receipt_from_google_ocr_json(json_ocr_kiwi)
    expected_sum = 62.60
    expected_products = [
      ReceiptProduct('vann med kullsyre', 4.90),
      ReceiptProduct('pant', 2.50),
      ReceiptProduct('vann med kullsyre', 4.90),
      ReceiptProduct('pant', 2.50),
      ReceiptProduct('frydenlund pilsner', 28.90),
      ReceiptProduct('pant', 2.00),
      ReceiptProduct('nypoteter', 16.90, quantity=dict(value=1.5, unit='kg')),
    ]

    self.assertEqual(receipt.get_sum(), expected_sum, f'Sum should be {expected_sum}')
    actual_products = receipt.get_all_products()
    self.assertEqual(len(actual_products), len(expected_products), f'Should find {len(expected_products)} products')
    for i, product in enumerate(actual_products):
      self.assertAlmostEqual(product.price, expected_products[i].price, msg=f'price is incorrect for {product}')
      if (expected_products[i].quantity):
        self.assertEqual(expected_products[i].quantity['value'], product.quantity['value'])

  def test_ikea_receipt(self):
    receipt = read_receipt_from_google_ocr_json(json_ocr_ikea)
    expected_sum = 368.00
    expected_products = [
      ReceiptProduct('sluka termokanne', 169.00),
      ReceiptProduct('gokart', 199.00),
    ]

    self.assertEqual(receipt.get_sum(), expected_sum, f'Sum should be {expected_sum}')
    actual_products = receipt.get_all_products()
    self.assertEqual(len(actual_products), len(expected_products), f'Should find {len(expected_products)} products')
    for i, product in enumerate(actual_products):
      self.assertAlmostEqual(product.price, expected_products[i].price, msg=f'price is incorrect for {product}')
      if (expected_products[i].quantity):
        self.assertEqual(expected_products[i].quantity['value'], product.quantity['value'])

  def test_prix_receipt(self):
    receipt = read_receipt_from_google_ocr_json(json_ocr_prix)
    expected_sum = 68.00
    expected_products = [
      ReceiptProduct('banan xtra', 10.43),
      ReceiptProduct('coop kidneybønner', 6.70),
      ReceiptProduct('coop kikerter', 5.50, quantity=dict(value=410, unit='g')),
      ReceiptProduct('coop tørkeruller', 45.20),
      ReceiptProduct('øreavrunding', 0.17),
    ]

    self.assertEqual(receipt.get_sum(), expected_sum, f'Sum should be {expected_sum}')
    actual_products = receipt.get_all_products()
    self.assertEqual(len(actual_products), len(expected_products), f'Should find {len(expected_products)} products')
    for i, product in enumerate(actual_products):
      self.assertAlmostEqual(product.price, expected_products[i].price, msg=f'price is incorrect for {product}')
      if (expected_products[i].quantity):
        self.assertEqual(expected_products[i].quantity['value'], product.quantity['value'])
