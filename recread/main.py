import json
import sys
import os
import time

from recread.gcloud.ocr import get_ocr_response_from_image_file, get_ocr_response_from_url
from recread.ocrresponses.lib import read_receipt_from_google_ocr_json

start_time = time.time()


receipt = read_receipt_from_google_ocr_json(get_ocr_response_from_url('gs://vfa-receipt-scanning_receipt-images/kvittering-kiwi.jpg'))

products = receipt.get_all_products()
print('Number of products found: {}'.format(len(products)))
print('Executed in {} seconds'.format(time.time() - start_time))

try:
    with open(os.path.join(os.path.dirname(__file__), 'output', 'outfile.json'), 'w') as outfile:
        json.dump([vars(x) for x in products], outfile, indent=2)
finally:
    outfile.close()
