class BoundUnaryExpression:
    def __init__(self, expressionType, operator, operand, text_span):
        self.expressionType = expressionType
        self.operator = operator
        self.operand = operand
        self.text_span = text_span
