import unittest

from recread.ocrresponses.lines import get_sorted_lines_by_x_axis


class TestLines(unittest.TestCase):
    def test_sort_by_x_axis(self):
        overlap_map = [
            [0, 1, 2],
            [2, 0],
        ]
        expected = [
            [1, 0, 2],
            [0, 2],
        ]
        text_annotations = [
            dict(boundingPoly=dict(vertices=[
                dict(x=10, y=100),
                dict(x=25, y=102),
                dict(x=24, y=140),
                dict(x=10, y=138),
            ])),
            dict(boundingPoly=dict(vertices=[
                dict(x=9, y=100),
                dict(x=25, y=102),
                dict(x=24, y=140),
                dict(x=10, y=138),
            ])),
            dict(boundingPoly=dict(vertices=[
                dict(x=20, y=100),
                dict(x=39, y=102),
                dict(x=40, y=140),
                dict(x=21, y=138),
            ])),
        ]
        actual = get_sorted_lines_by_x_axis(overlap_map, text_annotations)

        self.assertListEqual(actual, expected)
