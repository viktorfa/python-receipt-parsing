import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from receipt_scanning.Receipt import Receipt
from receipt_scanning.lib import read_receipt_from_google_ocr_json

with open('./receipt_scanning/tests/data/receipt_kiwi.json') as json_file:
  receipt = read_receipt_from_google_ocr_json(json.load(json_file), 0)


products = receipt.get_all_products()
print('Number of products found: {}'.format(len(products)))

try:
  with open('outfile.json', 'w') as outfile:
    json.dump([vars(x) for x in products], outfile)
finally:
  outfile.close()
