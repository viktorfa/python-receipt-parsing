import re

from recread.parsing.enums import token_types


price_pattern = r'\d+[,\.]\d{2}'
weight_pattern = r'\d+[,\.]\d{3}'
float_pattern = r'\d+[,\.]\d+'
int_pattern = r'(?<![,\.\d+])\d+(?![,\.\d+])'
vat_pattern = r'\d{1,2}\%'
product_text_pattern = r'[A-Za-z]+'
group_price_pattern = r'(' + price_pattern + r')'
group_weight_pattern = r'(' + weight_pattern + r')'
group_float_pattern = r'(' + float_pattern + r')'
group_int_pattern = r'(' + int_pattern + r')'
group_vat_pattern = r'(' + vat_pattern + r')'

compiled_group_price_pattern = re.compile(group_price_pattern)
compiled_group_weight_pattern = re.compile(group_weight_pattern)
compiled_group_float_pattern = re.compile(group_float_pattern)
compiled_group_int_pattern = re.compile(group_int_pattern)
compiled_group_vat_pattern = re.compile(group_vat_pattern)

quantity_units = (
    'g',
    'hg',
    'kg',
    'l',
    'ml',
    'dl',
    'stk',
)

sum_tokens = (
    'sum',
    'total',
    'nok',
)

unit_pattern = r'/?('
for i, x in enumerate(quantity_units):
    unit_pattern += x + r'|' if i < len(quantity_units) - 1 else x
unit_pattern += r')'

compiled_unit_pattern = re.compile(unit_pattern, re.IGNORECASE)

sum_pattern = r'('
for i, x in enumerate(sum_tokens):
    sum_pattern += x + r'|' if i < len(sum_tokens) - 1 else x
sum_pattern += r')'

compiled_sum_pattern = re.compile(sum_pattern, re.IGNORECASE)


def get_match_object_from_match(match):
    return dict(
        group=match.group(),
        end_pos=match.end(),
        start_pos=match.start(),
        match=match,
        string=match.string,
    )

def parse_float(string):
    return float(string.replace(',', '.'))

def find_float_type(float_match, unit_matches):
    for unit_match in unit_matches:
        if float_match['end_pos'] == unit_match['start_pos']:
            if unit_match['group'][0] == '/':
                return dict(
                    type=token_types.QUANTITY_UNIT_PRICE,
                    value=parse_float(float_match['group']),
                    unit=unit_match['group'][1:],
                    start_pos=float_match['start_pos'],
                    end_pos=float_match['end_pos'],
                    string=float_match['string'],
                )
            else:
                return dict(
                    type=token_types.QUANTITY,
                    value=parse_float(float_match['group']),
                    unit=unit_match['group'],
                    start_pos=float_match['start_pos'],
                    end_pos=float_match['end_pos'],
                    string=float_match['string'],
                )
    if is_sum(float_match):
        return dict(
            type=token_types.SUM,
            value=parse_float(float_match['group']),
            unit=None,
            start_pos=float_match['start_pos'],
            end_pos=float_match['end_pos'],
            string=float_match['string'],
        )
    elif is_product_price(float_match):
        return dict(
            type=token_types.PRODUCT_PRICE,
            value=parse_float(float_match['group']),
            unit=None,
            start_pos=float_match['start_pos'],
            end_pos=float_match['end_pos'],
            string=float_match['string'],
        )
    else:
        return dict(
            type=token_types.UNKNOWN,
            value=parse_float(float_match['group']),
            unit=None,
            start_pos=float_match['start_pos'],
            end_pos=float_match['end_pos'],
            string=float_match['string'],
        )

def is_product_price(float_match):
    # Whether there is a word with more the 2 letters in the line
    return len(get_product_name(float_match['string'][:float_match['start_pos']])) > 2 

def is_sum(float_match):
    if not re.match(price_pattern, float_match['group']):
        return False
    return compiled_sum_pattern.search(float_match['string'])

def find_int_type(int_match, unit_matches):
    for unit_match in unit_matches:
        if int_match['end_pos'] == unit_match['start_pos']:
            return dict(
                type=token_types.QUANTITY,
                value=int(int_match['group']),
                unit=unit_match['group'],
                start_pos=int_match['start_pos'],
                end_pos=int_match['end_pos'],
                string=int_match['string'],
            )
    if is_vat(int_match):
        return dict(
            type=token_types.VAT_PERCENTAGE,
            value=int(int_match['group']),
            unit=None,
            start_pos=int_match['start_pos'],
            end_pos=int_match['end_pos'],
            string=int_match['string'],
        )
    else:
        return dict(
            type=token_types.UNKNOWN,
            value=int(int_match['group']),
            unit=None,
            start_pos=int_match['start_pos'],
            end_pos=int_match['end_pos'],
            string=int_match['string'],
        )
    
def is_vat(int_match):
    if int_match['group'] not in ('0', '15', '25'):
        return False
    try:
        return int_match['string'][int_match['end_pos']] == '%'
    except IndexError:
        return False


def get_product_name(string_line):
    pattern = r'\D+'
    if not string_line:
        return ''
    candidates = re.findall(pattern, string_line)
    if not candidates:
        return ''
    return max(candidates, key=len)


def parse_token_line_floats(token_line):
    new_token_line = list([x for x in token_line])
    parsed_floats = []
    start_pos = 0
    for i, token in enumerate(token_line):
        if i == 0 or i == len(token_line) - 1:
            continue
        if i > 1:
            start_pos += len(token_line[i-2])
        prev_token = token_line[i-1]
        next_token = token_line[i+1]
        if re.match(r'^[,\.]$', token) and re.match(r'^\d+$', prev_token) and re.match(r'^\d+$', next_token):
            value = parse_float(prev_token + token + next_token)
            start_pos = start_pos
            end_pos = start_pos + len(prev_token) + len(token) + len(next_token)
            new_token_line[i-1] = None
            new_token_line[i] = None
            new_token_line[i+1] = None
            parsed_floats.append(dict(
                group=prev_token + token + next_token,
                string=''.join(token_line),
                start_pos=start_pos,
                end_pos=end_pos,
            ))
    return list([x for x in new_token_line if x]), parsed_floats