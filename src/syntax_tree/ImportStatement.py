from syntax_tree.Node import Node
from textSpan import TextSpan


class ImportStatement(Node):
    def __init__(self, importToken, filePath):
        self.token = importToken
        self.filePath = filePath
        start = importToken.text_span.start
        end = filePath.text_span.end
        self.text_span = TextSpan(start, end - start)

    def isInstance(self, *args):
        return self.token in args

    def getChildren(self):
        return [self.filePath]

    def get_txt(self):
        return self.token
