from syntax_tree.Node import Node
from token_handling.TokenTypes import TokenTypes


class ExpressionNode(Node):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"Value: [ {self.value} ], Token: [ {self.token} ]"

    def __repr__(self):
        return f"Value: [ {self.value} ], Token: [ {self.token} ]"

    def getChildren(self):
        return []

    def evaluate(self):
        if self.token.isInstance(TokenTypes.Variable):
            return self.value.evaluate()
        return self.value
