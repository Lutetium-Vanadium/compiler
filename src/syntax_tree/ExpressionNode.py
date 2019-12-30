from syntax_tree.Node import Node
from token_handling.TokenTypes import TokenTypes


class ExpressionNode(Node):
    def __init__(self, token):
        self.token_type = token.token_type
        self.value = token.value
        self.text_span = token.text_span

    def __repr__(self):
        return f"Value: [ {self.value} ], Token_Type: [ {self.token_type} ]"

    def __repr__(self):
        return f"Value: [ {self.value} ], Token_Type: [ {self.token_type} ]"

    def isInstance(self, *args):
        return self.token_type in args

    def getChildren(self):
        return []

    def updateValue(self, change):
        if self.isInstance(TokenTypes.Variable):
            self.value.value += change
        else:
            self.value += change
