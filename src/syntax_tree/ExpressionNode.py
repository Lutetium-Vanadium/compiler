from syntax_tree.Node import Node
from token_handling.TokenTypes import TokenTypes


class ExpressionNode(Node):
    def __init__(self, value, text_span=None, token_type=None, isList=False):
        if text_span == None:
            token_type = value.token_type
            text_span = value.text_span
            value = value.value

        self.token_type = token_type
        self.value = value
        self.text_span = text_span
        self.isList = isList

    def __repr__(self):
        return f"Value: {self.value}, Token_Type: <{self.token_type}>"

    def __repr__(self):
        return f"Value: {self.value}, Token_Type: <{self.token_type}>"

    def isInstance(self, *args):
        return self.token_type in args

    def getChildren(self):
        return []
