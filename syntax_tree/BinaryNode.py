from token_handling.TokenTypes import *
from syntax_tree.Node import Node
from textSpan import TextSpan


class BinaryNode(Node):
    def __init__(self, child1, child2, operatorToken):
        self.left = child1
        self.right = child2
        self.operatorToken = operatorToken
        start = left.text_span.start
        end = right.text_span.end
        self.text_span = TextSpan(start, end - start)

    def __repr__(self):
        return f"Children: {self.getChildren()}, OperatorToken: {self.operatorToken}"

    def __repr__(self):
        return f"Children: {self.getChildren()}, OperatorToken: {self.operatorToken}"

    def getChildren(self):
        return self.left, self.right


class BinaryOperatorNode(BinaryNode):
    def __init__(self, child1, child2, operatorToken):
        super().__init__(child1, child2, operatorToken)

    def evaluate(self):
        # Arithmetic Operators
        if self.operatorToken.token_type == TokenTypes.PlusOperator:
            return self.left.evaluate() + self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.MinusOperator:
            return self.left.evaluate() - self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.StarOperator:
            return self.left.evaluate() * self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.SlashOperator:
            return self.left.evaluate() / self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.ModOperator:
            return self.left.evaluate() % self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.CaretOperator:
            return self.left.evaluate() ** self.right.evaluate()

        # Boolean Operators
        if self.operatorToken.token_type == TokenTypes.OrOperator:
            return self.left.evaluate() or self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.AndOperator:
            return self.left.evaluate() and self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.NEOperator:
            return self.left.evaluate() != self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.EEOperator:
            return self.left.evaluate() == self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.GEOperator:
            return self.left.evaluate() >= self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.GTOperator:
            return self.left.evaluate() > self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.LEOperator:
            return self.left.evaluate() <= self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.LTOperator:
            return self.left.evaluate() < self.right.evaluate()
