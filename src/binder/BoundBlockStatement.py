class BoundBlockStatement:
    def __init__(self, expressionList, scope, text_span):
        self.type = expressionList[-1].type
        self.scope = scope
        self.children = expressionList
        self.text_span = text_span

    def __repr__(self):
        return f"BlockStatement: type={self.type}"

    def __repr__(self):
        return f"BlockStatement: type={self.type}"
