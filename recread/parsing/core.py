import operator

from recread.parsing.tokens import get_match_object_from_match, compiled_group_float_pattern, compiled_group_int_pattern, compiled_unit_pattern, find_float_type, find_int_type, parse_token_line_floats
from recread.parsing.enums import token_types

def parse_receipt_line(receipt_line):
    stripped_token_line, token_float_matches = parse_token_line_floats(receipt_line.token_line)
    stripped_string_line = ''.join(stripped_token_line)
    int_matches = [get_match_object_from_match(match) for match in compiled_group_int_pattern.finditer(stripped_string_line)]
    float_matches = [get_match_object_from_match(match) for match in compiled_group_float_pattern.finditer(stripped_string_line)]
    stripped_unit_matches = [get_match_object_from_match(match) for match in compiled_unit_pattern.finditer(stripped_string_line)]
    unit_matches = [get_match_object_from_match(match) for match in compiled_unit_pattern.finditer(receipt_line.string_line)]

    return [find_float_type(float_match, unit_matches) for float_match in token_float_matches] + [find_float_type(float_match, stripped_unit_matches) for float_match in float_matches] + [find_int_type(int_match, stripped_unit_matches) for int_match in int_matches]
