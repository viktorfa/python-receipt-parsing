import json

from recread.receipts.core import read_receipt_from_google_ocr_json
from recread.gcloud.ocr import get_ocr_response_from_url, get_ocr_response_from_image_file, store_and_get_ocr_response_from_base64_image_string


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
            get_ocr_response_from_url(event['queryStringParameters']['image_url']))
        response = {
            "statusCode": 200,
            "body": json.dumps([vars(x) for x in receipt.get_all_products()]),
            "headers": {
                'Access-Control-Allow-Origin': '*',
            }
        }
    except KeyError as e:
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
        receipt = read_receipt_from_google_ocr_json(
            store_and_get_ocr_response_from_base64_image_string(body))
        return {
            "statusCode": 200,
            "body": json.dumps([vars(x) for x in receipt.get_all_products()]),
            "headers": {
                'Access-Control-Allow-Origin': '*',
            }
        }
    except Exception as e:
        return get_error_response(500, 'Internal server error', str(e))
