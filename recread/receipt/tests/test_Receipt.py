import unittest
import json

from recread.receipt.models import Receipt, ReceiptLine
from recread.receipt.core import read_receipt_from_google_ocr_json

with open('./data/receipt_responses/kvittering-keiser-2.jpg.json') as keiser_json_file:
    keiser_json_object = json.load(keiser_json_file)


class Test_Receipt(unittest.TestCase):
    def test_can_instantiate(self):
        actual = read_receipt_from_google_ocr_json(keiser_json_object)
        self.assertIsInstance(actual, Receipt)

    def test_has_token_lines(self):
        actual = read_receipt_from_google_ocr_json(keiser_json_object)
        self.assertIsInstance(actual.token_lines, list)
        self.assertGreater(len(actual.token_lines), 0)

    def test_can_get_products(self):
        receipt = read_receipt_from_google_ocr_json(keiser_json_object)
        actual = receipt.get_all_products()
        self.assertIsInstance(actual, list)
        self.assertGreater(len(actual), 0)
        print('PRODUCTS')
        for product in actual:
            print(product)


class TestReceiptLine(unittest.TestCase):
    pass
