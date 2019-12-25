from TokenTypes import *

class BinaryNode():
    def __init__(self, child1, child2, operatorToken):
        self.left = child1
        self.right = child2
        self.operatorToken = operatorToken
    
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
        # Arthimetic Operators
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
        if self.operatorToken.token_type == TokenTypes.CarotOperator:
            return self.left.evaluate() ** self.right.evaluate()
        
        # Boolean Operators
        if self.operatorToken.token_type == TokenTypes.OrOperator:
            return self.left.evaluate() or self.right.evaluate()
        if self.operatorToken.token_type == TokenTypes.AndOperator:
            return self.left.evaluate() and self.right.evaluate()
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