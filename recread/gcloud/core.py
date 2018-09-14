import base64

from recread.gcloud.ocr import get_vision_client, get_ocr_response_from_url
from recread.gcloud.storage import store_image_in_gcloud

from recread.gcloud import config

def store_and_get_ocr_response_from_base64_image_string(base64string, client=get_vision_client()):
    image_bytes = base64.b64decode(base64string)
    image_file_name = store_image_in_gcloud(image_bytes)
    return get_ocr_response_from_url('gs://{bucket_name}/{file_name}'.format(
        bucket_name=config.BUCKET_NAME,
        file_name=image_file_name,
    ))