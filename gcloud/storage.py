import hashlib
import base64
import os

from google.cloud import storage
from google.cloud.storage.blob import Blob

from gcloud import config
from gcloud.util import generate_file_name


project_dir = os.path.join(os.path.dirname(__file__), '..')

credentials_folder = os.path.join(project_dir, '.credentials')
credentials_file_name = 'gcloud-credentials.json'




def get_storage_client():
    try:
        return storage.Client.from_service_account_json(
            os.path.join(credentials_folder, credentials_file_name)
        )
    except FileNotFoundError:
        return storage.Client()

def store_image_in_gcloud(image_bytes, client=get_storage_client()):
  bucket = client.get_bucket(config.BUCKET_NAME)
  file_name = generate_file_name(image_bytes)
  blob = bucket.blob(file_name)
  blob.upload_from_string(image_bytes, content_type='image/jpeg')
  return file_name