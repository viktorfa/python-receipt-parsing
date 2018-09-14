import io
import os
import json
import time
import base64

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson, MessageToDict

from gcloud import cache
from gcloud import config
from gcloud.storage import generate_file_name, store_image_in_gcloud

project_dir = os.path.join(os.path.dirname(__file__), '..')

credentials_folder = os.path.join(project_dir, '.credentials')
credentials_file_name = 'gcloud-credentials.json'
image_folder = os.path.join(project_dir, 'data', 'receipt_images')
output_folder = os.path.join(project_dir, 'data', 'receipt_responses')



def get_vision_client():
    try:
        return vision.ImageAnnotatorClient.from_service_account_json(
            os.path.join(credentials_folder, credentials_file_name)
        )
    except FileNotFoundError:
        return vision.ImageAnnotatorClient()

def get_ocr_response_from_image_file(image_file_name, client=get_vision_client()):
    with io.open(os.path.join(image_folder, image_file_name), 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    return MessageToDict(response)


def get_ocr_response_from_url(url, client=get_vision_client()):
    image = types.Image()
    image.source.image_uri = url
    response = client.document_text_detection(image=image)
    return MessageToDict(response)


def get_ocr_response_from_base64_image_string(base64string, client=get_vision_client()):
    image_bytes = base64.b64decode(base64string)
    image = types.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    return MessageToDict(response)


def store_and_get_ocr_response_from_base64_image_string(base64string, client=get_vision_client()):
    image_bytes = base64.b64decode(base64string)
    image_file_name = store_image_in_gcloud(image_bytes)
    return get_ocr_response_from_url('gs://{bucket_name}/{file_name}'.format(
        bucket_name=config.BUCKET_NAME,
        file_name=image_file_name,
    ))
