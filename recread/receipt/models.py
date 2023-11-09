from recread.parsing.core import parse_line, get_product_name


class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.token_lines = []
        for o in overlaps:
            self.token_lines.append(
                [text_annotations[i]["description"] for i in o if i != 0]
            )
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]
        self.generate_products()

    def get_all_products(self):
        return self.products

    def get_all_lines(self):
        return self.receipt_lines

    def generate_products(self):
        self.products = [
            product
            for product in [
                ReceiptProduct.from_receipt_line(x, i)
                for i, x in enumerate(self.receipt_lines)
            ]
            if product
        ]
        total_candidates = [
            product
            for product in self.products
            if "total" in product.name.lower() or "sum" in product.name.lower()
        ]
        self.implicit_total = None
        for x in total_candidates:
            if not self.implicit_total:
                self.implicit_total = x
            elif x.price > self.implicit_total.price:
                self.implicit_total = x

        tax_candidates = [
            product
            for product in self.products
            if "mva" in product.name.lower() or "moms" in product.name.lower()
        ]
        self.implicit_tax = None
        for x in tax_candidates:
            if not self.implicit_tax:
                self.implicit_tax = x

        self.products = list(
            [
                product
                for i, product in enumerate(self.products)
                if product.price
                <= (self.implicit_total.price if self.implicit_total else True)
                and not (
                    "mva" in product.name.lower() or "moms" in product.name.lower()
                )
                and (i < self.implicit_total.index if self.implicit_total else True)
            ]
        )


class ReceiptLine:
    def __init__(self, token_line):
        self.token_line = token_line
        self.string_line = "".join(token_line)
        self.parsed_line = parse_line(self.string_line)

    def __str__(self):
        return self.string_line


class ReceiptProduct:
    def __init__(
        self,
        name,
        price,
        index,
        unit_price=None,
        quantity=None,
        items_quantity=None,
    ):
        self.name = name
        self.price = price
        self.unit_price = unit_price
        self.quantity = quantity
        self.items_quantity = items_quantity
        self.index = index

    @classmethod
    def from_receipt_line(cls, receipt_line, index: int):
        price = None
        name = None
        for token in receipt_line.parsed_line:
            if token["type"] == "PRODUCT_PRICE":
                price = token["value"]
        name = get_product_name(receipt_line.string_line)
        if price:
            return ReceiptProduct(name, price, index=index)
        else:
            return None

    def __str__(self):
        return "{0}: {1}".format(self.name, self.price)


class ReceiptDbScan(Receipt):
    def __init__(self, annotation_lines):
        self.token_lines = []
        for annotation_line in annotation_lines:
            self.token_lines.append(
                [annotation["description"] for annotation in annotation_line]
            )
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]
        self.generate_products()


class ReceiptMongo(Receipt):
    def __init__(self, token_lines):
        self.token_lines = token_lines
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]
        self.generate_products()
