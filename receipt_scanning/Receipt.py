from parsing.lib import get_ngrams, find_prices, find_weights, find_unit_prices

class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.overlaps = overlaps
        self.text_annotations = text_annotations
        self.token_lines = []
        for o in overlaps:
            self.token_lines.append([text_annotations[i]['description'] for i in o if i != 0])
        self.string_lines = [' '.join(str(x)) for x in self.token_lines]
        self.receipt_lines = [ReceiptLine(x) for x in self.token_lines]

class ReceiptLine:
    def __init__(self, token_line):
        self.token_line = token_line
        self.receipt_trigrams = [ReceiptNgram(x) for x in get_ngrams(self.token_line, 3)]
        self.prices = []
        self.weights = []
        self.unit_prices = []
        for trigram in self.receipt_trigrams:
            self.prices.extend(trigram.prices)
            self.weights.extend(trigram.weights)
            self.unit_prices.extend(trigram.unit_prices)

class ReceiptNgram:
    def __init__(self, ngram):
        self.ngram = ngram
        self.prices = find_prices(ngram)
        self.weights = find_weights(ngram)
        self.unit_prices = find_unit_prices(ngram)

