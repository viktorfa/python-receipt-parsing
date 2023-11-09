from recread.util import get_distinct_lists
from recread.ocrresponses.rotation import straighten_annotations
from recread.ocrresponses.lines import (
    find_optimal_height_factor,
    get_overlap_map,
    get_sorted_lines_by_x_axis,
    get_sorted_lines_by_y_axis,
)
from recread.receipt.models import Receipt
from copy import deepcopy
from sklearn.cluster import DBSCAN
from sklearn import metrics
from recread.receipt.models import ReceiptDbScan
from recread.ocrresponses.util import get_y_center
import statistics


def read_receipt_from_google_ocr_json(json_dict):
    print("READING RECEIPT!!!")
    text_annotations = json_dict["text_annotations"]
    straighten_annotations(text_annotations)
    optimal_height_factor, _ = find_optimal_height_factor(text_annotations)
    overlap_map = get_overlap_map(text_annotations, optimal_height_factor / 10)
    distinct_overlaps = get_distinct_lists(overlap_map)
    sorted_distinct_overlaps = get_sorted_lines_by_x_axis(
        distinct_overlaps, text_annotations
    )
    sorted_distinct_lines = get_sorted_lines_by_y_axis(
        sorted_distinct_overlaps, text_annotations
    )
    print("Receipt ready")
    return Receipt(sorted_distinct_lines, text_annotations)


def read_receipt_from_google_ocr_json_dbscan(json_dict):
    print("READING RECEIPT!!!")
    text_annotations = deepcopy(json_dict["text_annotations"])
    straighten_annotations(text_annotations)

    annotation_heights = [
        abs(
            a["bounding_poly"]["vertices"][0]["y"]
            - a["bounding_poly"]["vertices"][2]["y"]
        )
        for a in text_annotations
    ]
    median_height = statistics.median(annotation_heights)
    text_annotations = [
        a
        for a in text_annotations
        if abs(
            a["bounding_poly"]["vertices"][0]["y"]
            - a["bounding_poly"]["vertices"][2]["y"]
        )
        < median_height * 3
    ]
    annotations_y = [
        sum(vert["y"] for vert in a["bounding_poly"]["vertices"][2:]) / 2
        for a in text_annotations
    ]
    annotations_y = list([x] for x in annotations_y)

    db_scans = []

    for x in range(1, 10):
        db = DBSCAN(eps=median_height / (x / 2), min_samples=1).fit(annotations_y)
        sil = metrics.silhouette_score(annotations_y, db.labels_)
        db_scans.append((db, sil))

    db, sil = sorted(db_scans, key=lambda x: x[1], reverse=True)[0]
    print(f"Best sil factor: {sil:.3f}")

    labels = db.labels_

    lines = {}

    for i, label in enumerate(labels):
        annotation = text_annotations[i]
        if label not in lines.keys():
            lines[label] = [annotation]
        else:
            lines[label].append(annotation)

    overlap_map = list(lines.values())
    for line in overlap_map:
        line = sorted(
            line,
            key=lambda x: min(
                x["bounding_poly"]["vertices"][0]["x"],
                x["bounding_poly"]["vertices"][3]["x"],
            ),
        )
    sorted_distinct_lines = sorted(
        overlap_map, key=lambda x: get_y_center(x[0]["bounding_poly"])
    )
    receipt = ReceiptDbScan(sorted_distinct_lines)
    return receipt
