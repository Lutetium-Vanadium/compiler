class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"
