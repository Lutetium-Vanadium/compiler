class BoundLiteralExpression:
    def __init__(self, expressionType, value, text_span):
        self.type = expressionType
        self.value = value
        self.text_span = text_span
