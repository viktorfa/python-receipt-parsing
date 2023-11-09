import boto3
import pynamodb

from recread.dynamodb.pynamo.models import GcvResponseModel, ReceiptLinesModel


def save_gcv_response(gcv_response, image_hash):
    db_object = GcvResponseModel(image_hash)
    return db_object.update(
        actions=[
            GcvResponseModel.gcv_response.set(gcv_response),
        ]
    )


def save_receipt_lines(receipt_lines_tokens, image_hash):
    db_object = ReceiptLinesModel(image_hash)
    return db_object.update(
        actions=[
            # ReceiptLinesModel.receipt_lines.set(receipt_lines),
            ReceiptLinesModel.receipt_lines_tokens.set(receipt_lines_tokens),
        ]
    )
