class BoundBinaryExpression:
    def __init__(self, expressionType, left, operator, right, text_span):
        self.expressionType = expressionType
        self.left = left
        self.operator = operator
        self.right = right
        self.text_span = text_span
