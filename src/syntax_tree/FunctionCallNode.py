from syntax_tree.Node import Node
from textSpan import TextSpan


class FunctionCallNode(Node):
    def __init__(self, token, params, token_type):
        self.name = token.value
        self.params = tuple(params)
        self.token_type = token_type
        start = token.text_span.start
        if len(params) > 0:
            end = params[-1].text_span.end + 1
        else:
            end = token.text_span.end + 2
        self.text_span = TextSpan(start, end - start)

    def __repr__(self):
        return f"Function: [ {self.name} ], Params: {self.params}"

    def __repr__(self):
        return f"Function: [ {self.name} ], Params: {self.params}"

    def isInstance(self, *args):
        return self.token_type in args

    def getChildren(self):
        return self.params

    def get_txt(self):
        return f"Function: {self.name}"
