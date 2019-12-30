from syntax_tree.AssignmentNode import AssignmentNode
from textSpan import TextSpan


class DeclarationNode(AssignmentNode):
    def __init__(self, declarationToken, assignmentNode):
        self.declarationKeyword = declarationToken.value
        self.identifier = assignmentNode.identifier
        self.expression = assignmentNode.expression
        self.operatorToken = assignmentNode.operatorToken
        start = declarationToken.text_span.start
        end = assignmentNode.text_span.end
        self.text_span = TextSpan(start, end - start)
