from syntax_tree.Node import Node


class Statement(Node):
    def __init__(self, expression):
        self.expression = expression
        self.text_span = expression.text_span

    def __repr__(self):
        return f"Expression: {self.expression}"

    def __str__(self):
        return f"Expression: {self.expression}"

    def getChildren(self):
        return self.expression
