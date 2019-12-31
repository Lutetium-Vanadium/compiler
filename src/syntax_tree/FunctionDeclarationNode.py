from textSpan import TextSpan
from token_handling.TokenTypes import TokenTypes
from syntax_tree.Node import Node


class FunctionDeclarationNode(Node):
    def __init__(self, declarationToken, identifier, params, functionBody):
        self.declarationKeyword = declarationToken.value
        self.identifier = identifier
        self.params = params
        self.functionBody = functionBody
        start = declarationToken.text_span.start
        end = functionBody.text_span.end
        self.text_span = TextSpan(start, end - start)

    def __repr__(self):
        return f"Function: [ {self.identifier.value} ], Params: {self.params}"

    def __repr__(self):
        return f"Function: [ {self.identifier.value} ], Params: {self.params}"

    def isInstance(self, *args):
        return TokenTypes.DeclarationKeyword in args

    def getChildren(self):
        return self.params

    def get_txt(self):
        return f"Function: {self.identifier.value}"
