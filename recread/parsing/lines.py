import operator

from recread.parsing.enums import token_types, line_types
from recread.parsing.tokens import get_product_name


def get_price_of_line(receipt_line):
    candidates = [x for x in receipt_line.parsed_line if x['type']
                  == token_types.PRODUCT_PRICE]
    if not candidates:
        return None
    return max(candidates, key=operator.itemgetter('end_pos'))


def get_line_type(receipt_line):
    occurences = {token_type: [] for token_type in (token_types.PRODUCT_PRICE,
                                                   token_types.QUANTITY,
                                                   token_types.QUANTITY_UNIT_PRICE, 
                                                   token_types.SUM, 
                                                   token_types.UNKNOWN, 
                                                   token_types.VAT_PERCENTAGE)}
    for x in receipt_line.parsed_line:
        occurences[x['type']].append(x)
    if occurences[token_types.QUANTITY] and occurences[token_types.QUANTITY_UNIT_PRICE]:
        return dict(
            type=line_types.MEASURE,
            price=occurences[token_types.QUANTITY_UNIT_PRICE][0],
            quantity=occurences[token_types.QUANTITY][0],
        )
    elif occurences[token_types.SUM]:
        return dict(
            type=line_types.TOTAL_SUM,
            price=occurences[token_types.SUM][0],
        )
    elif occurences[token_types.PRODUCT_PRICE] and is_product_price(receipt_line.string_line):
        return dict(
            type=line_types.PRODUCT,
            price=get_price_of_line(receipt_line),
            quantity=occurences[token_types.QUANTITY][0] if occurences[token_types.QUANTITY] else None,
        )
    else:
        return dict(
            type=line_types.UNKNOWN,
        )


def is_product_price(string, start=0, end=-1):
    # Whether there is a word with more the 2 letters in the line
    return len(get_product_name(string[start:end])) > 2
