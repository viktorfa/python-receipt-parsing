import os

from botocore.session import Session
from pynamodb.connection.base import Connection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute

from recread import config
from recread.serverless.common import is_in_aws_lambda


class GcvResponseModel(Model):
    class Meta:
        table_name = 'gcv_responses'
        region = config.AWS_REGION_DEFAULT

    image_hash = UnicodeAttribute(hash_key=True)
    gcv_response = MapAttribute(default=None)


class ReceiptLinesModel(Model):
    class Meta:
        table_name = 'receipt_lines'
        region = config.AWS_REGION_DEFAULT

    image_hash = UnicodeAttribute(hash_key=True)
    receipt_lines = ListAttribute(default=None)
    receipt_lines_tokens = ListAttribute(default=None)


def monkeypatch_connection(profile=config.AWS_PROFILE_DEFAULT):
    @property
    def session(self):
        if getattr(self._local, 'session', None) is None:
            self._local.session = Session(profile=profile)
        return self._local.session

    Connection.session = session



if not is_in_aws_lambda():
  monkeypatch_connection()
