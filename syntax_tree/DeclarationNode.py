from syntax_tree.AssignmentNode import AssignmentNode
from textSpan import TextSpan


class DeclarationNode(AssignmentNode):
    def fromAssignment(self, declarationKeyword, assignmentNode):
        self.declarationKeyword = declarationKeyword
        self.identifier = assignmentNode.identifier
        self.expression = assignmentNode.expression
        self.operatorToken = assignmentNode.operatorToken
        start = declarationKeyword.text_span.start
        end = assignmentNode.text_span.end
        self.text_span = TextSpan(start, end - start)
