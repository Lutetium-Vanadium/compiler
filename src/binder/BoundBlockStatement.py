from binder.BoundNode import BoundNode


class BoundBlockStatement(BoundNode):
    def __init__(self, expressionList, scope, block_type, text_span, functional=False):
        self.type = block_type
        self.scope = scope
        self.children = expressionList
        self.text_span = text_span
        self.functional = functional

    def __repr__(self):
        if self.functional:
            return f"BoundFunctionStatement => <{self.type}>"
        return f"BlockStatement: <{self.type}>"

    def __repr__(self):
        if self.functional:
            return f"BoundFunctionStatement => <{self.type}>"
        return f"BlockStatement: <{self.type}>"

    def get_txt(self):
        return self.__str__()

    def get_children(self):
        return self.children
