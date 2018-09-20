from recread.parsing.core import parse_line, get_product_name

class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.overlaps = overlaps
        self.text_annotations = text_annotations
        self.token_lines = []
        for o in overlaps:
            self.token_lines.append([text_annotations[i]['description'] for i in o if i != 0])
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]

    def get_all_products(self):
        return [product for product in [ReceiptProduct.from_receipt_line(x) for x in self.receipt_lines] if product]

    def get_all_lines(self):
        return self.receipt_lines

class ReceiptLine:
    def __init__(self, token_line):
        self.token_line = token_line
        self.string_line = ''.join(token_line)
        self.parsed_line = parse_line(self.string_line)

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

