from recread.util import get_distinct_lists
from recread.ocrresponses.rotation import straighten_annotations
from recread.ocrresponses.lines import find_optimal_height_factor, get_overlap_map, get_sorted_lines_by_x_axis, get_sorted_lines_by_y_axis
from recread.receipt.models import Receipt


def read_receipt_from_google_ocr_json(json_dict):
    print('READING RECEIPT!!!')
    text_annotations = json_dict['textAnnotations']
    straighten_annotations(text_annotations)
    optimal_height_factor, _ = find_optimal_height_factor(text_annotations)
    overlap_map = get_overlap_map(text_annotations, optimal_height_factor / 10)
    distinct_overlaps = get_distinct_lists(overlap_map)
    sorted_distinct_overlaps = get_sorted_lines_by_x_axis(distinct_overlaps, text_annotations)
    sorted_distinct_lines = get_sorted_lines_by_y_axis(sorted_distinct_overlaps, text_annotations)
    return Receipt(sorted_distinct_lines, text_annotations)