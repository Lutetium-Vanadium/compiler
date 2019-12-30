from binder.BoundNode import BoundNode


class BoundReturnStatement(BoundNode):
    def __init__(self, to_return, text_span):
        self.to_return = to_return
        self.text_span = text_span
        self.type = to_return.type

    def __repr__(self):
        return f"return <{self.type}>"

    def __repr__(self):
        return f"return <{self.type}>"

    def get_children(self):
        return [self.to_return]

    def get_txt(self):
        return f"BoundReturnStatement => <{self.type}>"
