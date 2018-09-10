import os
import json

responses_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'receipt_responses')




def get_response_by_image_name(image_name):
  try:
    with open('{}.json'.format(os.path.join(responses_folder, image_name)), 'r') as json_file:
      return json.load(json_file)
  except IOError:
    return None

def get_response_by_url(url):
  image_name = url.split('/')[-1]
  try:
    with open('{}.json'.format(os.path.join(responses_folder, image_name)), 'r') as json_file:
      return json.load(json_file)
  except IOError:
    return None