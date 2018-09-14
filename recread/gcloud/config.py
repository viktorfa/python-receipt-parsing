import os

from recread import config

BUCKET_NAME = 'vfa-receipt-scanning_receipt-images'
CREDENTIALS_FILE_PATH = os.path.join(config.PROJECT_DIR, '.credentials', 'gcloud-credentials.json')