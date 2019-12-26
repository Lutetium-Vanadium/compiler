from token_handling.TokenTypes import *
from syntax_tree.Node import Node


class UnaryNode(Node):
    def __init__(self, child, operatorToken):
        self.child = child
        self.operatorToken = operatorToken

    def __repr__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"

    def __str__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"

    def getChildren(self):
        return (self.child,)


class UnaryOperatorNode(UnaryNode):
    def __init__(self, child, operatorToken):
        super().__init__(child, operatorToken)

    def evaluate(self):
        if self.operatorToken.isInstance(TokenTypes.MinusOperator):
            return -self.child.evaluate()

        if self.operatorToken.isInstance(TokenTypes.NotOperator):
            return not self.child.evaluate()

        if self.operatorToken.isInstance(TokenTypes.PlusPlusOperator):
            self.child.updateValue(1)

        if self.operatorToken.isInstance(TokenTypes.MinusMinusOperator):
            self.child.updateValue(-1)

        return self.child.evaluate()
