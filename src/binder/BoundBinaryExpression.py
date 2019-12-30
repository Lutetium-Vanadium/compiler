from binder.BoundNode import BoundNode


class BoundBinaryExpression(BoundNode):
    def __init__(self, expressionType, left, operator, right, text_span):
        self.type = expressionType
        self.left = left
        self.operator = operator
        self.right = right
        self.text_span = text_span

    def __repr__(self):
        return f"Left: {self.left}, Operator: {self.operator}, Right: {self.right}"

    def __str__(self):
        return f"Left: {self.left}, Operator: {self.operator}, Right: {self.right}"

    def get_children(self):
        return [self.left, self.right]

    def get_txt(self):
        return f"BoundBinaryExpression {self.operator.value} - <{self.type}>"
