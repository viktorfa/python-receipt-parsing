import unittest
import json

from recread.receipt.models import Receipt, ReceiptLine
from recread.receipt.core import read_receipt_from_google_ocr_json
from recread.receipt.models import ReceiptMongo

with open("./data/receipt_responses/kvittering-keiser.jpg.json") as keiser_json_file:
    keiser_json_object = json.load(keiser_json_file)
with open("./data/receipt_responses/kvittering-keiser.jpg.json") as keiser_json_file:
    keiser_receipt_lines = json.load(keiser_json_file)


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
        print("PRODUCTS")
        for product in actual:
            print(product)

    def test_can_get_products_2(self):
        receipt = ReceiptMongo(
            [
                ["KEISER", "FRUKTMARKED", "AS"],
                ["ORG.NR", "980", "371", "611"],
                ["Torvgata", "12", ",", "2000", "Lillestrøm"],
                ["Man", "-", "Fre", "08-20"],
                ["Lør", "08-19", "Søn", "10-19"],
                ["Tlf", ":", "64", "84", "51", "20"],
                ["2", "x", "19.90NOK"],
                ["Vårløk", "39.80NOK"],
                ["5", "x", "9.90NOK"],
                ["Agurk", "49.50NOK"],
                ["DIV", "GRØNT", ",", "STK", "15.00NOK"],
                ["1.032", "kg", "@", "99.90", "NOK", "/", "kg"],
                ["Tomater", "Cherry"],
                ["#", "20100", "103.10NOK"],
                ["1.790", "kg", "@", "12.90", "NOK", "/", "kg"],
                ["#", "20052", "Løk", "23.10NOK"],
                ["1.806", "kg", "@", "17.90", "NOK", "/", "kg"],
                ["#", "20055", "Lok", "rød", "32.30NOK"],
                ["Hvitløk", "500g", "14.90NOK"],
                ["2", "x", "14.90NOK"],
                ["Issalat", "29.80NOK"],
                ["Salat", "Ruccula", "14.90NOK"],
                ["2", "x", "1.00NOK"],
                ["Pose", "2.00NOK"],
                ["Total", "324.00NOK"],
                ["MVA", "15", "%", "42.00NOK"],
                ["MVA", "0", "%", "0.00NOK"],
                ["BANKKORT", "324.00NOK"],
                ["13:03", "13.05.2023", "1", "Kasse", "1", "504"],
                ["Takk", "for", "kjøpet", "!"],
                ["POS3", "sn", ":", "2540166", "ver.:6.3.18.14"],
                ["***", "PARTNER", "KUPONG", "***"],
                ["15", "%", "rabatt", "på", "alle", "varer", "hos", ":"],
                ["www.elskerkaffe.no", ",", "ved", "bruk", "av"],
                ["rabattkoden", ":", "«", "KEISER", "»"],
            ]
        )
        actual = receipt.get_all_products()
        self.assertIsInstance(actual, list)
        self.assertGreater(len(actual), 0)
        print("PRODUCTS")
        for product in actual:
            print(product)

        print(receipt.implicit_total)
        print(receipt.implicit_tax)


class TestReceiptLine(unittest.TestCase):
    pass
