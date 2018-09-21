import math

from recread.parsing.core import parse_receipt_line
from recread.parsing.lines import get_price_of_line, get_line_type
from recread.parsing.tokens import get_product_name
from recread.parsing.enums import line_types, token_types


def get_value_unit_dict(d):
    return {key: value for key, value in d.items() if key in ('value', 'unit')} if d else None


class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.overlaps = overlaps
        self.text_annotations = text_annotations
        self.token_lines = []
        self.products = []
        for o in overlaps:
            self.token_lines.append(
                [text_annotations[i]['description'] for i in o if i != 0])
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]
        self.populate_products()

    def get_all_products(self):
        return self.products

    def get_all_lines(self):
        return self.receipt_lines

    def get_sum(self):
        for x in self.receipt_lines:
            if x.type == line_types.TOTAL_SUM:
                return x.price['value']
        return None

    def populate_products(self):
        measure_candidates = [
            x for x in self.receipt_lines if x.type == line_types.MEASURE]

        for receipt_line in self.receipt_lines:
            if receipt_line.type == line_types.TOTAL_SUM:
                # Assume all products are before the sum
                break
            elif receipt_line.type != line_types.PRODUCT:
                # Skip not product lines
                continue
            product = receipt_line
            product_kwargs = dict(
                name=get_product_name(product.string_line),
                price=product.price['value'],
                quantity=get_value_unit_dict(product.quantity),
            )
            for i, measure in enumerate(measure_candidates):
                if math.isclose(measure.price['value'] * measure.quantity['value'], product.price['value'], abs_tol=.01):
                    product_kwargs.update(dict(
                        unit_price=get_value_unit_dict(measure.price),
                        quantity=get_value_unit_dict(measure.quantity),
                    ))
                    measure_candidates.pop(i)
                    break
            self.products.append(ReceiptProduct(**product_kwargs))

    def get_json_dict(self):
        return dict(
            products=[x.__dict__ for x in self.get_all_products()],
            sum=self.get_sum(),
        )


class ReceiptLine:
    def __init__(self, token_line):
        self.token_line = token_line
        self.string_line = ''.join(token_line)
        self.parsed_line = parse_receipt_line(self)
        line_type = get_line_type(self)
        self.type = line_type['type']
        if self.type == line_types.PRODUCT:
            self.price = line_type['price']
            self.quantity = line_type['quantity']
        elif self.type == line_types.TOTAL_SUM:
            self.price = line_type['price']
        elif self.type == line_types.MEASURE:
            self.price = line_type['price']
            self.quantity = line_type['quantity']
        else:
            self.price = None

    def __str__(self):
        return self.string_line


class ReceiptProduct:
    def __init__(self, name, price, unit_price=None, quantity=None, items_quantity=None):
        self.name = name
        self.price = price
        self.unit_price = unit_price
        self.quantity = quantity
        self.items_quantity = items_quantity

    @classmethod
    def from_receipt_line(self, receipt_line):
        price = None
        name = None
        for token in receipt_line.parsed_line:
            if token['type'] == 'PRODUCT_PRICE':
                price = token['value']
        name = get_product_name(receipt_line.string_line)
        if price:
            return ReceiptProduct(name, price)
        else:
            return None

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.price)
