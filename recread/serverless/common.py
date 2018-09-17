import os

def is_in_aws_lambda():
  return not not os.getenv('AWS_REGION')


def is_lambda_local():
  return not not os.getenv('IS_LOCAL')
