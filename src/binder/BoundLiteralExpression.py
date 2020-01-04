from binder.BoundNode import BoundNode


class BoundLiteralExpression(BoundNode):
    def __init__(self, expressionType, value, text_span, isList):
        self.type = expressionType
        self.value = value
        self.text_span = text_span
        self.isList = isList

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def get_txt(self):
        return f"BoundLiteral '{self.value}' - <{self.type}>"
