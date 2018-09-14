import hashlib
import base64
import os

from google.cloud import storage
from google.cloud.storage.blob import Blob

from recread import config
from recread.gcloud import config as gcloud_config
from recread.gcloud.util import generate_file_name

def get_storage_client():
    try:
        return storage.Client.from_service_account_json(gcloud_config.CREDENTIALS_FILE_PATH)
    except FileNotFoundError:
        return storage.Client()

def store_image_in_gcloud(image_bytes, client=get_storage_client()):
  bucket = client.get_bucket(gcloud_config.BUCKET_NAME)
  file_name = generate_file_name(image_bytes)
  blob = bucket.blob(file_name)
  blob.upload_from_string(image_bytes, content_type='image/jpeg')
  return file_name