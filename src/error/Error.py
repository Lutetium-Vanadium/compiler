class Error:
    def __init__(self, text, text_span):
        self.text = text
        self.text_span = text_span

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text
