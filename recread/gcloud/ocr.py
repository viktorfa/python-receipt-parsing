import io
import os
import json
import time
import base64

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict

from recread import config
from recread.gcloud import config as gcloud_config
from recread.gcloud.storage import generate_file_name, store_image_in_gcloud
from recread.serverless.common import is_lambda_local
from recread.gcloud.mocks import get_vision_client_mock

def get_vision_client():
    if is_lambda_local():
        return get_vision_client_mock()
    try:
        return vision.ImageAnnotatorClient.from_service_account_json(gcloud_config.CREDENTIALS_FILE_PATH)
    except FileNotFoundError:
        return vision.ImageAnnotatorClient()

def get_ocr_response_from_image_file(image_bytes, client=get_vision_client()):
    image = types.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    try:
        return MessageToDict(response)
    except Exception:
        return response


def get_ocr_response_from_url(url, client=get_vision_client()):
    image = types.Image()
    image.source.image_uri = url
    response = client.document_text_detection(image=image)
    try:
        return MessageToDict(response)
    except Exception:
        return response


def get_ocr_response_from_base64_image_string(base64string, client=get_vision_client()):
    image_bytes = base64.b64decode(base64string)
    image = types.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    try:
        return MessageToDict(response)
    except Exception:
        return response


def store_and_get_ocr_response_from_base64_image_string(base64string, client=get_vision_client()):
    image_bytes = base64.b64decode(base64string)
    image_file_name = store_image_in_gcloud(image_bytes)
    return get_ocr_response_from_url('gs://{bucket_name}/{file_name}'.format(
        bucket_name=gcloud_config.BUCKET_NAME,
        file_name=image_file_name,
    ))


def store_and_get_ocr_response_from_image_bytes(image_bytes, client=get_vision_client()):
    image_file_name = store_image_in_gcloud(image_bytes)
    return get_ocr_response_from_url('gs://{bucket_name}/{file_name}'.format(
        bucket_name=gcloud_config.BUCKET_NAME,
        file_name=image_file_name,
    ))