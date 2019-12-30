from syntax_tree.Node import Node
from textSpan import TextSpan


class FunctionNode(Node):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        start = name.text_span.start
        if len(params) > 0:
            end = params[-1].text_span.end
        else:
            end = name.text_span.end
        self.text_span = TextSpan(start, end - start)
