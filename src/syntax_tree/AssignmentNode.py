from syntax_tree.Node import Node
from token_handling.TokenTypes import TokenTypes
from textSpan import TextSpan


class AssignmentNode(Node):
    def __init__(self, identifier, expression, operatorToken):
        self.identifier = identifier
        self.expression = expression
        self.operatorToken = operatorToken
        start = identifier.text_span.start
        end = expression.text_span.end
        self.text_span = TextSpan(start, start - end)

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"

    def getChildren(self):
        return self.identifier, self.expression
