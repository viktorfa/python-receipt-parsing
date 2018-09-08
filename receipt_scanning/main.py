import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from receipt_scanning.Receipt import Receipt
from receipt_scanning.lib import read_receipt_from_google_ocr_json

with open('./receipt_scanning/tests/data/receipt_keiser.json') as json_file:
  receipt = read_receipt_from_google_ocr_json(json.load(json_file))

print(receipt.token_lines)