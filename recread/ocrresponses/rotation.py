import math

from recread.ocrresponses.util import get_x_length, get_y_length, get_poly_center, get_y_top_diff

def tilt_poly_straight(ocr_poly):
    top_y_diff = get_y_top_diff(ocr_poly)
    
    ocr_poly['vertices'][0]['y'] -= top_y_diff / 2
    ocr_poly['vertices'][1]['y'] += top_y_diff / 2
    ocr_poly['vertices'][2]['y'] += top_y_diff / 2
    ocr_poly['vertices'][3]['y'] -= top_y_diff / 2

def find_skew_angle(ocr_poly):
    left_bottom = ocr_poly['vertices'][3]
    right_bottom = ocr_poly['vertices'][2]
    
    # Do cosine trigonometry
    b = right_bottom['x'] - left_bottom['x']
    c = left_bottom['y'] - right_bottom['y']
    a = math.sqrt(b**2 + c**2)
    
    if left_bottom['y'] < right_bottom['y']:
        return math.acos((a**2 + b**2 - c**2) / (2 * a * b))
    else:
        return - math.acos((a**2 + b**2 - c**2) / (2 * a * b))
    
    
    
def straighten_polys(ocr_polys, angle, center=(0, 0)):
    for poly in ocr_polys:
        rotate_poly(poly, angle, center)
        
def straighten_annotations(annotations):
    angle = get_estimated_skew_angle([x['boundingPoly'] for x in annotations])
    center = (annotations[0]['boundingPoly']['vertices'][0]['x'], annotations[0]['boundingPoly']['vertices'][0]['y'])
    for annotation in annotations:
        rotate_poly(annotation['boundingPoly'], angle, center)
        
        
        
def get_estimated_skew_angle(polys, n=10):
    n_longest = sorted(polys, key=get_x_length, reverse=True)[:min(n, len(polys))]
    result = sum([find_skew_angle(p) for p in n_longest]) / len(n_longest)
    return result

def rotate_poly(ocr_poly, angle, center=(0, 0)):
    sin = math.sin(angle)
    cos = math.cos(angle)
    for p in ocr_poly['vertices']:
        x = p['x']
        y = p['y']
        centered_x = x - center[0]
        centered_y = y - center[1]
        rotated_x = centered_x * cos + centered_y * sin
        rotated_y = -centered_x * sin + centered_y * cos
        p['x'] = rotated_x + center[0]
        p['y'] = rotated_y + center[1]

def get_straight_poly(ocr_poly, center=(0, 0)):
    return get_rotated_poly(ocr_poly, find_skew_angle(ocr_poly), get_poly_center(ocr_poly))

def get_rotated_poly(ocr_poly, angle, center=(0, 0)):
    sin = math.sin(angle)
    cos = math.cos(angle)
    new_vertices = []
    for i, p in enumerate(ocr_poly['vertices']):
        x = p['x']
        y = p['y']
        centered_x = x - center[0]
        centered_y = y - center[1]
        rotated_x = centered_x * cos - centered_y * sin
        rotated_y = centered_x * sin + centered_y * cos
        result_x = rotated_x + center[0]
        result_y = rotated_y + center[1]
        new_vertices.append(dict(
            x=result_x,
            y=result_y,
        ))
    return {'vertices': new_vertices}
