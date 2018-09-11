import hashlib
import base64
import os

from google.cloud import storage
from google.cloud.storage.blob import Blob

from gcloud import config


project_dir = os.path.join(os.path.dirname(__file__), '..')

credentials_folder = os.path.join(project_dir, '.credentials')
credentials_file_name = 'gcloud-credentials.json'


try:
    client = storage.Client.from_service_account_json(
        os.path.join(credentials_folder, credentials_file_name)
    )
except FileNotFoundError:
    client = storage.Client()

def generate_file_name(image_bytes):
    m = hashlib.sha256()
    m.update(image_bytes)
    return '{}.jpg'.format(m.hexdigest())

def store_image_in_gcloud(image_bytes):
  bucket = client.get_bucket(config.BUCKET_NAME)
  file_name = generate_file_name(image_bytes)
  blob = bucket.blob(file_name)
  blob.upload_from_string(image_bytes, content_type='image/jpeg')
  return file_name