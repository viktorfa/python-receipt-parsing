import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.container import Container
from matplotlib.collections import PatchCollection

def plot_annotations(annotations, num_annotations=sys.maxsize):
    full_text_poly = get_plt_poly(annotations[0]['boundingPoly'])
    max_x = max([p[0] for p in full_text_poly])
    max_y = max([p[1] for p in full_text_poly])
    min_x = min([p[0] for p in full_text_poly])
    min_y = min([p[1] for p in full_text_poly])
    fig, ax = plt.subplots(figsize=(max_x/200, max_y/200), dpi=96)
    ax.set_xlim(min(0, min_x), max_x)
    ax.set_ylim(max_y, min(0, min_y))
    ax.xaxis.tick_top()
    patches = []
    num_annotations = min(1000, len(annotations))
    num_sides = 4

    for i in range(0, num_annotations):
        polygon = Polygon(get_plt_poly(annotations[i]['boundingPoly']))
        patches.append(polygon)
    p = PatchCollection(patches)

    colors = 100*np.random.rand(len(patches))
    p.set_array(np.array(colors))

    ax.add_collection(p)
    #plt.show()
    return fig, ax

def get_plt_poly(ocr_poly):
    return [(p['x'] if 'x' in p.keys() else 0, p['y'] if 'y' in p.keys() else 0) for p in ocr_poly['vertices']]



def plot_annotations_with_lines(receipt):
    fig, ax = plot_annotations(receipt.text_annotations)
    overlap_lines = [get_overlap_line(x, receipt.text_annotations) for x in receipt.overlaps if x]
    #ax.add_collection(PatchCollection([Line2D((x[0][0], x[1][0]), (x[0][1], x[1][1])) for x in overlap_lines]))
    #fig.lines.extend([Line2D((x[0][0], x[1][0]), (x[0][1], x[1][1])) for x in overlap_lines])
    for line in [Line2D((x[0][0], x[1][0]), (x[0][1], x[1][1]), color='black') for x in overlap_lines]:
        ax.add_line(line)
    plt.show()

def get_overlap_line(overlap, annotations, skip_first=True):
    return (get_left_y_center(annotations[overlap[1 if skip_first and len(overlap) > 0 else 0]]['boundingPoly']), get_right_y_center(annotations[overlap[-1]]['boundingPoly']))

def get_left_y_center(ocr_poly):
  return (ocr_poly['vertices'][0]['x'], ocr_poly['vertices'][0]['y'] + abs(ocr_poly['vertices'][3]['y'] - ocr_poly['vertices'][0]['y']) / 2)

def get_right_y_center(ocr_poly):
    return (ocr_poly['vertices'][1]['x'], ocr_poly['vertices'][1]['y'] + abs(ocr_poly['vertices'][2]['y'] - ocr_poly['vertices'][1]['y']) / 2)