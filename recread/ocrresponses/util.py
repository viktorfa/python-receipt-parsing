def get_poly_center(ocr_poly):
    return (get_x_center(ocr_poly), get_y_center(ocr_poly))

def get_x_length(ocr_poly):
    return abs(ocr_poly['vertices'][0]['x'] - ocr_poly['vertices'][1]['x'])

def get_y_length(ocr_poly):
    return abs(ocr_poly['vertices'][0]['y'] - ocr_poly['vertices'][2]['y'])

def get_y_top_diff(ocr_poly):
    return ocr_poly['vertices'][0]['y'] - ocr_poly['vertices'][1]['y']

def get_y_height(ocr_poly):
    return abs(ocr_poly['vertices'][0]['y'] - ocr_poly['vertices'][3]['y'])

def get_y_center(ocr_poly):
    return sum([p['y'] for p in ocr_poly['vertices']]) / 4

def get_x_center(ocr_poly):
    return sum([p['x'] for p in ocr_poly['vertices']]) / 4

def get_height(a):
    return a[1] - a[0]
