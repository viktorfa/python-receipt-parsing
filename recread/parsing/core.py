import re

from recread.parsing.lib import compiled_group_float_pattern, compiled_group_int_pattern, get_float_match_type, get_int_match_type

def parse_line(line):
    parsed_floats = compiled_group_float_pattern.finditer(line)
    parsed_ints = compiled_group_int_pattern.finditer(line)

    float_results = [get_float_match_type(f, line) for f in parsed_floats]
    int_results = [get_int_match_type(f, line) for f in parsed_ints]

    return float_results + int_results

def get_product_name(string_line):
    pattern = r'\D+'
    if not string_line:
        return ''
    candidates = re.findall(pattern, string_line)
    if not candidates:
        return ''
    return max(candidates, key=len)
