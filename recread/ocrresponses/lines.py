from functools import partial

from recread.util import get_distinct_lists
from recread.ocrresponses.util import get_y_height, get_y_center


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


def get_sorted_lines_by_x_axis(overlap_map, text_annotations):
    return [sorted(x, key=partial(overlap_group_sort, text_annotations=text_annotations)) for x in overlap_map]

def get_sorted_lines_by_y_axis(overlaps, annotations):
    return sorted(overlaps, key=lambda x: get_y_center(annotations[x[0]]['boundingPoly']))

def overlap_group_sort(i, text_annotations):
    return min(text_annotations[i]['boundingPoly']['vertices'][0]['x'], text_annotations[i]['boundingPoly']['vertices'][3]['x'])