from binder.BoundNode import BoundNode


class BoundWhileStatement(BoundNode):
    def __init__(self, condition, whileBlock, text_span):
        self.condition = condition
        self.whileBlock = whileBlock
        self.text_span = text_span
        self.type = whileBlock.type

    def __repr__(self):
        return f"if {self.condition} => {self.thenBlock} else => {self.elseBlock}"

    def __repr__(self):
        return f"if {self.condition} => {self.thenBlock} else => {self.elseBlock}"

    def get_children(self):
        return [self.condition, self.whileBlock]

    def get_txt(self):
        return f"BoundWhileCondition"
