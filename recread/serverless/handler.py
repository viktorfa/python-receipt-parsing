import json
import base64
import traceback

from recread.util import hash_bytes
from recread.receipt.core import read_receipt_from_google_ocr_json
from recread.gcloud.ocr import get_ocr_response_from_url, store_and_get_ocr_response_from_image_bytes
from recread.dynamodb.core import save_gcv_response, save_receipt_lines


def get_error_response(status_code=500, status_text='Internal server error', message=None):
    response_body = {
        "statusCode": status_code,
        "statusText": status_text,
        "message": message,
    }
    return {
        "statusCode": status_code,
        "statusText": status_text,
        "body": json.dumps(response_body),
    }


def hello(event, context):
    http_method = event['httpMethod']

    if http_method == 'GET':
        return handle_get(event, context)
    elif http_method == 'POST':
        return handle_post(event, context)
    else:
        return get_error_response(405, 'Unsupported method', 'Use GET or POST')


def handle_get(event, context):
    try:
        receipt = read_receipt_from_google_ocr_json(
            get_ocr_response_from_url(
                event['queryStringParameters']['image_url'])
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(receipt.get_json_dict()),
            "headers": {
                'Access-Control-Allow-Origin': '*',
            }
        }
    except KeyError as e:
        traceback.print_exc()
        return {
            "statusCode": 400,
            "statusText": "Bad request",
            "body": str(e),
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 500,
            "body": str(e)
        }

    return response


def handle_post(event, context):
    body = event['body']

    if not body:
        return get_error_response(400, 'Bad request', 'No request body. Should be b64 encoded image.')

    try:
        image_bytes = base64.b64decode(body)
        image_hash = hash_bytes(image_bytes)
        ocr_response = store_and_get_ocr_response_from_image_bytes(image_bytes)
        save_gcv_response(ocr_response, image_hash)

        receipt = read_receipt_from_google_ocr_json(ocr_response)
        save_receipt_lines(receipt.overlaps, receipt.token_lines, image_hash)

        return {
            "statusCode": 200,
            "body": json.dumps(receipt.get_json_dict()),
            "headers": {
                'Access-Control-Allow-Origin': '*',
            }
        }
    except Exception as e:
        traceback.print_exc()
        return get_error_response(500, 'Internal server error', str(e))
