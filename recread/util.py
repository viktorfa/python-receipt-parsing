import json
import hashlib

def get_distinct_lists(list_of_lists):
    hashable_lists = []
    for l in list_of_lists:
        json_list = json.dumps(l)
        if json_list not in hashable_lists:
            hashable_lists.append(json_list)
    return [json.loads(x) for x in hashable_lists]


def hash_bytes(byte_string):
    m = hashlib.blake2s()
    m.update(byte_string)
    return m.hexdigest()
    