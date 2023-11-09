import os
import pymongo
import logging
import datetime
from recread.receipt.models import Receipt
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from typing import Optional


logging.getLogger("pymongo").setLevel(logging.WARNING)

MONGO_URI = os.environ["MONGO_URI"]
MONGO_DATABASE = os.environ["MONGO_DATABASE"]
GRAPHQL_URL = os.environ["GRAPHQL_URL"]
HASURA_ADMIN_SECRET = os.environ["HASURA_ADMIN_SECRET"]

mongo_client = None
mongo_db = None


def get_collection(collection_name: str):
    global mongo_client
    global mongo_db
    logging.debug(
        f"Getting collection {collection_name} from {MONGO_URI} {MONGO_DATABASE}"
    )
    if mongo_client is None:
        mongo_client = pymongo.MongoClient(MONGO_URI)
    if mongo_db is None:
        mongo_db = mongo_client.get_database(MONGO_DATABASE)
    return mongo_db.get_collection(collection_name)


def save_gcv_response(gcv_response, image_hash: str):
    now = datetime.datetime.now()
    collection = get_collection("gcv_responses")
    return collection.insert_one(
        {
            "text_annotations": gcv_response["text_annotations"],
            "full_text": gcv_response["full_text_annotation"]["text"],
            "image_hash": image_hash,
            "updated_at": now,
            "created_at": now,
        }
    )


transport = RequestsHTTPTransport(
    url=GRAPHQL_URL,
    verify=True,
    retries=3,
    headers={"x-hasura-admin-secret": HASURA_ADMIN_SECRET},
)

gql_client = Client(transport=transport, fetch_schema_from_transport=True)


def save_receipt_lines(
    image_hash: str,
    org_id: Optional[str],
    gcv_response_id: str,
    full_text: str,
):
    query = gql(
        """
        mutation INSERT_RECEIPT($object: receipts_insert_input!) {
            insert_receipts_one(object: $object) {
                id
            }
        }
        """
    )
    insert_response = gql_client.execute(
        query,
        variable_values={
            "object": {
                "full_text": full_text,
                "gcv_response_id": gcv_response_id,
                "image_hash": image_hash,
                "org": org_id,
            }
        },
    )

    print("insert_response")
    print(insert_response)
    print(type(insert_response))

    return insert_response
