import json

def get_distinct_lists(list_of_lists):
    hashable_lists = []
    for l in list_of_lists:
        json_list = json.dumps(l)
        if json_list not in hashable_lists:
            hashable_lists.append(json_list)
    return [json.loads(x) for x in hashable_lists]