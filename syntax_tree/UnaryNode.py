from TokenTypes import *

class UnaryNode():
    def __init__(self, child, operatorToken):
        self.child = child
        self.operatorToken = operatorToken
    
    def __repr__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"
    
    def __str__(self):
        return f"Child: {self.child}, OperatorToken: {self.operatorToken}"

class UnaryOperatorNode(UnaryNode):
    def __init__(self, child, operatorToken):
        super().__init__(child, operatorToken)
    
    def evaluate(self):
        if self.operatorToken.token_type == TokenTypes.MinusOperator:
            return -self.child.evaluate()
        
        return self.child.evaluate()