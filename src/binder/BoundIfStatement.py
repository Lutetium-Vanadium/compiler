from binder.BoundNode import BoundNode
from type_handling.Types import Types


class BoundIfStatement(BoundNode):
    def __init__(self, condition, thenBlock, elseBlock, text_span):
        self.condition = condition
        self.thenBlock = thenBlock
        self.elseBlock = elseBlock
        self.text_span = text_span
        self.type = thenBlock.type

    def __repr__(self):
        return f"if {self.condition} => {self.thenBlock} else => {self.elseBlock}"

    def __repr__(self):
        return f"if {self.condition} => {self.thenBlock} else => {self.elseBlock}"

    def get_children(self):
        if self.elseBlock:
            return [self.condition, self.thenBlock, self.elseBlock]
        return [self.condition, self.thenBlock]

    def get_txt(self):
        return f"BoundIfCondition"
