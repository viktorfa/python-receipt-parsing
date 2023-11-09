import re

price_pattern = r"\d+[,\.]\d{2}"
weight_pattern = r"\d+[,\.]\d{3}"
float_pattern = r"\d+[,\.]\d+"
int_pattern = r"(?<![,\.\d+])\d+(?![,\.\d+])"
vat_pattern = r"\d{1,2}\%"
product_text_pattern = r"[A-Za-z]+"
group_price_pattern = r"(" + price_pattern + r")"
group_weight_pattern = r"(" + weight_pattern + r")"
group_float_pattern = r"(" + float_pattern + r")"
group_int_pattern = r"(" + int_pattern + r")"
group_vat_pattern = r"(" + vat_pattern + r")"

compiled_group_price_pattern = re.compile(group_price_pattern)
compiled_group_weight_pattern = re.compile(group_weight_pattern)
compiled_group_float_pattern = re.compile(group_float_pattern)
compiled_group_int_pattern = re.compile(group_int_pattern)
compiled_group_vat_pattern = re.compile(group_vat_pattern)

quantity_units = (
    "g",
    "hg",
    "kg",
    "l",
    "ml",
    "dl",
    "stk",
)

unit_pattern = r"/?("
for i, x in enumerate(quantity_units):
    unit_pattern += x + r"|" if i < len(quantity_units) - 1 else x
unit_pattern += r")"

compiled_unit_pattern = re.compile(unit_pattern)


def get_float_match_type(match, line):
    if is_price(match, line):
        return dict(
            type="PRODUCT_PRICE",
            value=float(match.group().replace(",", ".")),
            unit=None,
            start_pos=match.start(),
            end_pos=match.end(),
        )
    else:
        return get_match_suffix(match, line)


def get_int_match_type(match, line):
    return get_match_suffix(match, line)


def is_price(match, line):
    return re.match(r"" + price_pattern + r"$", match.group())


def get_match_suffix(match, line):
    unit_match = compiled_unit_pattern.match(line, match.end(), match.end() + 4)

    if unit_match:
        return dict(
            unit=unit_match.group()[1:]
            if line[match.end()] == "/"
            else unit_match.group(),
            value=float(match.group().replace(",", ".")),
            type="QUANTITY_UNIT_PRICE" if line[match.end()] == "/" else "QUANTITY_UNIT",
            start_pos=match.start(),
            end_pos=unit_match.end(),
        )
    else:
        return dict(
            type=None,
            value=float(match.group().replace(",", ".")),
            start_pos=match.start(),
            end_pos=match.end(),
            unit=None,
        )
