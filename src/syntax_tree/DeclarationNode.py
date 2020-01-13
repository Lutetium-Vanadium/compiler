from syntax_tree.AssignmentNode import AssignmentNode
from textSpan import TextSpan


class DeclarationNode(AssignmentNode):
    def __init__(self, declarationToken, identifier, expression, operatorToken):
        self.declarationKeyword = declarationToken.value
        self.identifier = identifier
        self.expression = expression
        self.operatorToken = operatorToken
        start = declarationToken.text_span.start
        if expression != None:
            end = expression.text_span.end
        else:
            end = identifier.text_span.end
        self.text_span = TextSpan(start, end - start)
