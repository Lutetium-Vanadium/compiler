from token_handling.TokenTypes import *
from syntax_tree.Node import Node
from textSpan import TextSpan


class UnaryNode(Node):
    def __init__(self, child, operatorToken):
        self.child = child
        self.operatorToken = operatorToken
        start = operatorToken.text_span.start
        end = child.text_span.end
        self.text_span = TextSpan(start, start - end)

    def __repr__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"

    def __str__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"

    def getChildren(self):
        return (self.child,)


class UnaryOperatorNode(UnaryNode):
    def __init__(self, child, operatorToken):
        super().__init__(child, operatorToken)
