import io
import os
import json
import time
import base64

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson, MessageToDict

from recread import config
from recread.gcloud import config as gcloud_config
from recread.gcloud.storage import generate_file_name, store_image_in_gcloud

def get_vision_client():
    try:
        return vision.ImageAnnotatorClient.from_service_account_json(gcloud_config.CREDENTIALS_FILE_PATH)
    except FileNotFoundError:
        return vision.ImageAnnotatorClient()

def get_ocr_response_from_image_file(image_bytes, client=get_vision_client()):
    image = types.Image(content=image_bytes)
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
        bucket_name=gcloud_config.BUCKET_NAME,
        file_name=image_file_name,
    ))