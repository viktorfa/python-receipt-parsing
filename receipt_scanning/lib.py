import json
from functools import partial

from receipt_scanning.Receipt import Receipt

def read_receipt_from_google_ocr_json(json_dict, OVERLAP_SAME_LINE_LIMIT=20):
    text_annotations = json_dict['responses'][0]['textAnnotations']
    full_text_with_y_axis = [(annotation['description'], (annotation['boundingPoly']['vertices'][0]['y'], annotation['boundingPoly']['vertices'][2]['y'])) for annotation in text_annotations]
    overlap_map = get_overlap_map(full_text_with_y_axis, OVERLAP_SAME_LINE_LIMIT)
    distinct_overlaps = get_distinct_lists(overlap_map)
    sorted_distinct_overlaps = sort_overlap_groups_by_x_axis(distinct_overlaps, text_annotations)
    return Receipt(sorted_distinct_overlaps, text_annotations)
    
    
def get_overlap_map(full_text_with_y_axis, OVERLAP_SAME_LINE_LIMIT=20):
    result = [[] for _ in full_text_with_y_axis]
    for i, (_, a) in enumerate(full_text_with_y_axis):
        for j, (_, b) in enumerate(full_text_with_y_axis):
            overlap_size = get_overlap_size(a, b)
            if overlap_size >= OVERLAP_SAME_LINE_LIMIT:
                result[i].append(j)
                
    return result
    
def get_height(a):
    return a[1] - a[0]

def get_overlap_size(a, b):
    return min(a[1] - b[0], b[1] - a[0], get_height(a), get_height(b))

def get_distinct_lists(list_of_lists):
    hashable_lists = []
    for l in list_of_lists:
        json_list = json.dumps(l)
        if json_list not in hashable_lists:
            hashable_lists.append(json_list)
    return [json.loads(x) for x in hashable_lists]

def sort_overlap_groups_by_x_axis(overlap_map, text_annotations):
    return [sorted(x, key=partial(overlap_group_sort, text_annotations=text_annotations)) for x in overlap_map]

def overlap_group_sort(i, text_annotations):
    return min(text_annotations[i]['boundingPoly']['vertices'][0]['x'], text_annotations[i]['boundingPoly']['vertices'][3]['x'])
