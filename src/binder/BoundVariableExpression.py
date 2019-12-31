from binder.BoundNode import BoundNode


class BoundVariableExpression(BoundNode):
    def __init__(self, name, varType, text_span):
        self.type = varType
        self.name = name
        self.text_span = text_span

    def __repr__(self):
        return f"BoundVariable '{self.name}' - <{self.type}>"

    def __str__(self):
        return f"BoundVariable '{self.name}' - <{self.type}>"

    def get_txt(self):
        return f"BoundVariable '{self.name}' - <{self.type}>"
