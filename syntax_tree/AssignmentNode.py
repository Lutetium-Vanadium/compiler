from syntax_tree.Node import Node


class AssignmentNode(Node):
    def __init__(self, identifier, expression, operatorToken):
        self.identifier = identifier
        self.expression = expression
        self.operatorToken = operatorToken

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"

    def __repr__(self):
        return f"Variable {self.identifier} = {self.expression}"

    def getChildren(self):
        return self.identifier, self.expression

    def evaluate(self):
        return self.identifier.evaluate()
