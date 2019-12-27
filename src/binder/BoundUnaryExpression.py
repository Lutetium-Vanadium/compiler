class BoundUnaryExpression:
    def __init__(self, expressionType, operator, operand, text_span):
        self.type = expressionType
        self.operator = operator
        self.operand = operand
        self.text_span = text_span

    def __repr__(self):
        return f"Child: {self.operator}, OperatorToken: {self.operatorToken}"

    def __str__(self):
        return f"Child: {self.operator}, OperatorToken: {self.operatorToken}"
