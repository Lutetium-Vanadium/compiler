from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundUnaryExpression import BoundUnaryExpression

from variables.VariableBag import VariableBag
from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types


class Evaluator:
    def __init__(self, syntaxTree, variables: VariableBag):
        self.syntaxTree = syntaxTree
        self.variables = variables

    def evaluate(self):
        return self.evaluateNode(self.syntaxTree)

    def evaluateNode(self, node):
        if isinstance(node, BoundAssignmentExpression):
            return self.evaluateAssignmentExpression(node)

        if isinstance(node, BoundBinaryExpression):
            return self.evaluateBinaryExpression(node)

        if isinstance(node, BoundUnaryExpression):
            return self.evaluateUnaryExpression(node)

        if isinstance(node, BoundLiteralExpression):
            return self.evaluateLiteralExpression(node)

        if isinstance(node, BoundVariableExpression):
            return self.evaluateVariableExpression(node)

        if isinstance(node, BoundDeclarationExpression):
            return self.evaluateDeclarationExpression(node)

    def evaluateAssignmentExpression(self, node: BoundAssignmentExpression):
        return node.varValue

    def evaluateBinaryExpression(self, node: BoundBinaryExpression):
        # Arithmetic Operators
        if node.operator.isInstance(TokenTypes.PlusOperator):
            return self.evaluateNode(node.left) + self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.MinusOperator):
            return self.evaluateNode(node.left) - self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.StarOperator):
            return self.evaluateNode(node.left) * self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.SlashOperator):
            if node.type == Types.Int:
                return self.evaluateNode(node.left) // self.evaluateNode(node.right)
            return self.evaluateNode(node.left) / self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.ModOperator):
            return self.evaluateNode(node.left) % self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.CaretOperator):
            return self.evaluateNode(node.left) ** self.evaluateNode(node.right)

        # Boolean Operators
        if node.operator.isInstance(TokenTypes.OrOperator):
            return self.evaluateNode(node.left) or self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.AndOperator):
            return self.evaluateNode(node.left) and self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.NEOperator):
            return self.evaluateNode(node.left) != self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.EEOperator):
            return self.evaluateNode(node.left) == self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.GEOperator):
            return self.evaluateNode(node.left) >= self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.GTOperator):
            return self.evaluateNode(node.left) > self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.LEOperator):
            return self.evaluateNode(node.left) <= self.evaluateNode(node.right)
        if node.operator.isInstance(TokenTypes.LTOperator):
            return self.evaluateNode(node.left) < self.evaluateNode(node.right)

    def evaluateDeclarationExpression(self, node: BoundDeclarationExpression):
        return node.varValue

    def evaluateLiteralExpression(self, node: BoundLiteralExpression):
        return node.value

    def evaluateVariableExpression(self, node: BoundVariableExpression):
        success, var = self.variables.tryGetVariable(node.var.name)
        if success:
            return self.evaluateNode(var.value)

        # All non declared variables should be taken care of in the binder
        raise NameError(f"Variable {node.var.name} doesn't exist.")

    def evaluateUnaryExpression(self, node: BoundUnaryExpression):
        if node.operator.isInstance(TokenTypes.MinusOperator):
            return -(self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.NotOperator):
            return not (self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.PlusPlusOperator):
            self.variables.updateValue(
                node.operand.var.name, self.evaluateNode(node.operand) + 1
            )

        if node.operator.isInstance(TokenTypes.MinusMinusOperator):
            self.child.updateValue(
                node.operand.var.name, self.evaluateNode(node.operand) - 1
            )

        return self.evaluateNode(node.operand)
