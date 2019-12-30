from syntax_tree.Node import Node
from textSpan import TextSpan


class ReturnStatement(Node):
    def __init__(self, token, to_return):
        self.token = token
        self.to_return = to_return
        start = self.token.text_span.start
        end = self.to_return.text_span.end
        self.text_span = TextSpan(start, end - start)

    def isInstance(self, *args):
        return self.token in args

    def getChildren(self):
        return [self.to_return]

    def get_txt(self):
        return self.token
