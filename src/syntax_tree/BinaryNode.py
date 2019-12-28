from token_handling.TokenTypes import *
from syntax_tree.Node import Node
from textSpan import TextSpan


class BinaryNode(Node):
    def __init__(self, left, right, operatorToken):
        self.left = left
        self.right = right
        self.operatorToken = operatorToken
        start = left.text_span.start
        end = right.text_span.end
        self.text_span = TextSpan(start, end - start)

    def __repr__(self):
        return f"Children: {self.getChildren()}, OperatorToken: {self.operatorToken}"

    def __repr__(self):
        return f"Children: {self.getChildren()}, OperatorToken: {self.operatorToken}"

    def getChildren(self):
        return self.left, self.right


class BinaryOperatorNode(BinaryNode):
    def __init__(self, left, right, operatorToken):
        super().__init__(left, right, operatorToken)
