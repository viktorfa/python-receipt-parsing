from recread.parsing.lib import get_ngrams, find_prices, find_weights, find_unit_prices, is_product, find_prices_in_string

class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.overlaps = overlaps
        self.text_annotations = text_annotations
        self.token_lines = []
        for o in overlaps:
            self.token_lines.append([text_annotations[i]['description'] for i in o if i != 0])
        self.string_lines = [' '.join(str(x)) for x in self.token_lines]
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]

    def get_all_products(self):
        return [x.product for x in self.receipt_lines if x.product]

class ReceiptLine:
    def __init__(self, token_line):
        self.token_line = token_line
        self.string_line = ''.join(token_line)
        self.prices = []
        self.weights = []
        self.unit_prices = []
        self.prices = find_prices_in_string(self.string_line)
        self.weights = find_weights(self.token_line)
        self.unit_prices = find_unit_prices(self.token_line)

        if is_product(self):
            self.product = ReceiptProduct(''.join(self.string_line[:self.prices[-1]['start_pos']]), self.prices[-1]['value'])
        else:
            self.product = None

class ReceiptProduct:
    def __init__(self, name, price, unit_price=None, quantity=None, items_quantity=None):
        self.name = name
        self.price = price
        self.unit_price = unit_price
        self.quantity = quantity
        self.items_quantity = items_quantity

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.price)

