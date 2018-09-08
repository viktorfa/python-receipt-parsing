class Receipt:
    def __init__(self, overlaps, text_annotations):
        self.overlaps = overlaps
        self.text_annotations = text_annotations
        self.token_lines = []
        for o in overlaps:
            self.token_lines.append([text_annotations[i]['description'] for i in o if i != 0])
        self.string_lines = [' '.join(str(x)) for x in self.token_lines]
