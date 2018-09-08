import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from receipt_scanning.Receipt import Receipt
from receipt_scanning.lib import read_receipt_from_google_ocr_json

receipt_folder = os.path.join('.', 'data', 'receipts')
file_name = 'receipt_kiwi.json'

with open(os.path.join(receipt_folder, file_name)) as json_file:
  receipt = read_receipt_from_google_ocr_json(json.load(json_file), 15)


products = receipt.get_all_products()
print('Number of products found: {}'.format(len(products)))

try:
  with open('./output/outfile.json', 'w') as outfile:
    json.dump([vars(x) for x in products], outfile)
finally:
  outfile.close()
