from binder.BoundNode import BoundNode


class BoundAssignmentExpression(BoundNode):
    def __init__(self, expressionType, varName, varValue, text_span):
        self.type = expressionType
        self.varName = varName
        self.varValue = varValue
        self.text_span = text_span

    def __repr__(self):
        return f"Variable {self.varName} = {self.varValue}"

    def __repr__(self):
        return f"Variable {self.varName} = {self.varValue}"

    def get_txt(self):
        return f"BoundAssignment for '{self.varName}' - <{self.type}>"

    def get_children(self):
        return [self.varValue]
