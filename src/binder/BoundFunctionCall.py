from binder.BoundNode import BoundNode


class BoundFunctionCall(BoundNode):
    def __init__(self, name, params, return_type, text_span):
        self.name = name
        self.params = params
        self.type = return_type
        self.text_span = text_span

    def __repr__(self):
        return f"BoundFunctionCall '{self.name}' - <{self.type}>"

    def __str__(self):
        return f"BoundFunctionCall '{self.name}' - <{self.type}>"

    def get_txt(self):
        return f"BoundFunctionCall '{self.name}' - <{self.type}>"
