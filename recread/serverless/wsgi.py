import base64
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from recread.receipt.core import (
    read_receipt_from_google_ocr_json,
    read_receipt_from_google_ocr_json_dbscan,
)
from recread.gcloud.ocr import (
    get_ocr_response_from_url,
    store_and_get_ocr_response_from_image_bytes,
)
from recread.util import hash_bytes
from recread.mongo.core import save_gcv_response, save_receipt_lines, get_collection
from recread.receipt.models import ReceiptMongo
import logging
import jwt
import os
import traceback
import datetime
from google.cloud import storage
from recread.gcloud import config as gcloud_config


logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
CORS(app)


@app.route("/v1/status", methods=["GET"])
def get_status():
    return jsonify({"status": "OK"}), 200


@app.route("/v1/status/mongo", methods=["GET"])
def get_mongo_status():
    collection = get_collection("receipts_data")
    document = collection.find_one()
    return jsonify({"status": "OK", "document": document}), 200


@app.route("/v1/receipt", methods=["GET"])
@cross_origin()
def receipt_with_image_url():
    org_id = None
    try:
        token = get_jwt_claims(request)
        org_id = token["x-hasura-org-id"]
    except Exception as e:
        logging.warn("Error")
        print(e)
    image_url = request.args.get("image_url")
    if not image_url:
        return jsonify({"error": "Missing image_url parameter"}), 400
    ocr_response = get_ocr_response_from_url(image_url)
    receipt = read_receipt_from_google_ocr_json_dbscan(ocr_response)
    return jsonify([vars(x) for x in receipt.get_all_products()])


@app.route("/v1/receipt", methods=["POST"])
def receipt_with_post_body():
    org_id = None
    try:
        token = get_jwt_claims(request)
        print("token")
        print(token)
        org_id = token["x-hasura-org-id"]
    except Exception as e:
        logging.warn("Error")
        print(e)

    image_b64 = request.data
    image_bytes = base64.b64decode(image_b64)
    image_hash = hash_bytes(image_bytes)

    existing_response = get_collection("parsed_receipts").find_one(
        {"image_hash": image_hash}
    )
    if existing_response:
        logging.info("Found existing response")
        receipt = ReceiptMongo(existing_response["token_lines"])
        return jsonify([vars(x) for x in receipt.get_all_products()])

    ocr_response = store_and_get_ocr_response_from_image_bytes(image_bytes)
    save_response_result = save_gcv_response(ocr_response, image_hash=image_hash)
    gcv_response_id = save_response_result.inserted_id
    # receipt = read_receipt_from_google_ocr_json_dbscan(ocr_response)
    save_receipt_lines(
        image_hash=image_hash,
        org_id=org_id,
        gcv_response_id=str(gcv_response_id),
        full_text=ocr_response["full_text_annotation"]["text"],
    )
    return jsonify(dict(image_hash=image_hash))


@app.route("/v1/storage/<file>", methods=["GET"])
def get_signed_url(file: str):
    storage_client = storage.Client.from_service_account_json(
        gcloud_config.CREDENTIALS_FILE_PATH
    )
    bucket = storage_client.bucket(gcloud_config.BUCKET_NAME)
    blob = bucket.blob(file)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    return jsonify({"url": url}), 200


def get_jwt_claims(request):
    jwt_token = request.headers.get("Authorization").split(" ")[1]
    token = jwt.decode(
        jwt_token,
        key=os.environ["JWT_SECRET"],
        algorithms=[os.environ["JWT_ALG"]],
    )
    claims = token["https://hasura.io/jwt/claims"]
    return {k.lower(): v for k, v in claims.items()}
