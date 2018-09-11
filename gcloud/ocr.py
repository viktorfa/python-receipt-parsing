import io
import os
import json
import time
import base64

from google.protobuf.json_format import MessageToJson, MessageToDict
from google.cloud import vision
from google.cloud.vision import types
from google.auth import credentials

from gcloud import cache

project_dir = os.path.join(os.path.dirname(__file__), '..')

credentials_folder = os.path.join(project_dir, '.credentials')
credentials_file_name = 'gcloud-credentials.json'
image_folder = os.path.join(project_dir, 'data', 'receipt_images')
output_folder = os.path.join(project_dir, 'data', 'receipt_responses')


try:
    client = vision.ImageAnnotatorClient.from_service_account_json(
        os.path.join(credentials_folder, credentials_file_name)
    )
except FileNotFoundError:
    client = vision.ImageAnnotatorClient()

def get_ocr_response_from_image_file(image_file_name):
    response = cache.get_response_by_image_name(image_file_name)
    if response:
        print('Loading {} from cache'.format(image_file_name))
        return response
    else:
        output_file_name = '{image_file}.json'.format(image_file=image_file_name)
        with io.open(os.path.join(image_folder, image_file_name), 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        try:
            with open(os.path.join(output_folder, output_file_name), 'w') as output_file:
                output_file.write(MessageToJson(response))
        finally:
            if not output_file.closed:
                output_file.close()
        return MessageToDict(response)

def get_ocr_response_from_url(url, use_files=False):
    if use_files:
        response = cache.get_response_by_url(url)
        if response:
            print('Loading {} from cache'.format(url))
            return response
        else:
            output_file_name = '{image_file}.json'.format(image_file=url.split('/')[-1])
            image = types.Image()
            image.source.image_uri = url
            response = client.document_text_detection(image=image)
            try:
                with open(os.path.join(output_folder, output_file_name), 'w') as output_file:
                    output_file.write(MessageToJson(response))
            finally:
                if not output_file.closed:
                    output_file.close()
            return MessageToDict(response)
    else:
        image = types.Image()
        image.source.image_uri = url
        response = client.document_text_detection(image=image)
        return MessageToDict(response)


def get_ocr_response_from_base64_image_string(base64string):
    image_bytes = base64.b64decode(base64string)
    image = types.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    return MessageToDict(response)