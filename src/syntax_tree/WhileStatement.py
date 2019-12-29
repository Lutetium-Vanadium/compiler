from syntax_tree.Node import Node
from textSpan import TextSpan


class WhileStatement(Node):
    def __init__(self, whileToken, condition, whileBlock):
        self.token = whileToken
        self.condition = condition
        self.whileBlock = whileBlock
        start = whileToken.text_span.start
        end = whileBlock.text_span.end
        self.text_span = TextSpan(start, end - start)

    def isInstance(self, *args):
        return self.token in args

    def getChildren(self):
        return [self.condition, self.whileBlock]

    def get_txt(self):
        return self.token
