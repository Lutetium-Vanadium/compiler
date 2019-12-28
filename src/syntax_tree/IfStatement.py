from syntax_tree.Node import Node
from textSpan import TextSpan


class IfStatement(Node):
    def __init__(self, ifToken, condition, thenBlock, elseBlock):
        self.token = ifToken
        self.condition = condition
        self.thenBlock = thenBlock
        self.elseBlock = elseBlock
        start = ifToken.text_span.start
        if elseBlock:
            end = elseBlock.text_span.end
        else:
            end = thenBlock.text_span.end
        self.text_span = TextSpan(start, end - start)

    def isInstance(self, *args):
        return self.token in args

    def getChildren(self):
        if self.elseBlock:
            return [self.condition, self.thenBlock, self.elseBlock]
        return [self.condition, self.thenBlock]

    def get_txt(self):
        return self.token
