import json
from functools import partial

from recread.receipt_scanning.Receipt import Receipt
from recread.receipt_scanning.rotation import straighten_annotations

def read_receipt_from_google_ocr_json(json_dict):
    print('READING RECEIPT!!!')
    text_annotations = json_dict['textAnnotations']
    straighten_annotations(text_annotations)
    optimal_height_factor, _ = find_optimal_height_factor(text_annotations)
    overlap_map = get_overlap_map(text_annotations, optimal_height_factor / 10)
    distinct_overlaps = get_distinct_lists(overlap_map)
    sorted_distinct_overlaps = sort_overlap_groups_by_x_axis(distinct_overlaps, text_annotations)
    sorted_distinct_lines = get_sorted_lines_by_y_axis(sorted_distinct_overlaps, text_annotations)
    return Receipt(sorted_distinct_lines, text_annotations)

def find_optimal_height_factor(annotations):
    height_factors = range(1, 17, 2)
    results = []
    
    for hf in height_factors:
        results.append((hf, len(get_distinct_lists(get_overlap_map(annotations, hf / 10)))))
        if len(results) > 1 and results[-1][1] == results[-2][1]:
            print(results)
            return results[-1]
        elif len(results) > 1 and results[-1][1] > results[-2][1]:
            print(results)
            return results[-2]
    print('Could not find optimal height factor')
    print(results)
    return results[-1]
    
def get_overlap_map(annotations, height_factor=.6):
    result = [[] for _ in annotations]
    for i, a in enumerate(annotations):
        a_y_center = get_y_center(a['boundingPoly'])
        a_height = get_y_height(a['boundingPoly'])
        for j, b in enumerate(annotations):
            b_y_center = get_y_center(b['boundingPoly'])
            b_height = get_y_height(b['boundingPoly'])
            
            ab_dist_center = abs(a_y_center - b_y_center)
            ab_min_height = min(a_height, b_height)
            ab_max_height = max(a_height, b_height)
            
            ab_is_same_line = ab_dist_center < ab_min_height * height_factor and ab_max_height < ab_min_height * 5
            
            if ab_is_same_line:
                result[i].append(j)
    return result

def get_y_height(ocr_poly):
    return abs(ocr_poly['vertices'][0]['y'] - ocr_poly['vertices'][3]['y'])

def get_y_center(ocr_poly):
    return sum([p[1] for p in get_poly_from_ocr_poly(ocr_poly)]) / 4

def get_poly_from_ocr_poly(ocr_poly):
    return ((p['x'], p['y']) for p in ocr_poly['vertices'])

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

def get_sorted_lines_by_y_axis(overlaps, annotations):
    return sorted(overlaps, key=lambda x: get_y_center(annotations[x[0]]['boundingPoly']))

def overlap_group_sort(i, text_annotations):
    return min(text_annotations[i]['boundingPoly']['vertices'][0]['x'], text_annotations[i]['boundingPoly']['vertices'][3]['x'])
