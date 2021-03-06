from binder.BoundNode import BoundNode


class BoundBlockStatement(BoundNode):
    def __init__(self, expressionList, scope, block_type, text_span, isFunction):
        self.type = block_type
        self.scope = scope
        self.children = expressionList
        self.text_span = text_span
        self.isFunction = isFunction

    def __repr__(self):
        return f"BoundBlockStatement: <{self.type}>"

    def __repr__(self):
        return f"BoundBlockStatement: <{self.type}>"

    def addVariables(self, lst):
        for arg in lst:
            self.scope.addOrReplace(arg, arg.name)

    def copy(self):
        return BoundBlockStatement(
            self.children, self.scope, self.type, self.text_span, self.isFunction
        )

    def get_txt(self):
        return self.__str__()

    def get_children(self):
        return self.children
