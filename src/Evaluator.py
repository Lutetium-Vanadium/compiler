from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundUnaryExpression import BoundUnaryExpression

from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types


class Evaluator:
    def __init__(self, syntaxTree, scope):
        self.syntaxTree = syntaxTree
        self.scope = scope

    def evaluate(self):
        return self.evaluateNode(self.syntaxTree)

    def evaluateNode(self, node):
        if isinstance(node, BoundBlockStatement):
            return self.evaluateBlockStatement(node)

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

    def evaluateBlockStatement(self, node):
        value = None
        for boundExpression in node.children:
            value = self.evaluateNode(boundExpression)
        return value

    def evaluateAssignmentExpression(self, node):
        self.scope.updateValue(
            node.varName, self.evaluateNode(node.varValue), node.varValue.text_span
        )
        return self.scope.tryGetVariable(node.varName)[1]

    def evaluateBinaryExpression(self, node):
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

    def evaluateDeclarationExpression(self, node):
        # For Declaration, value need not be updated as the binder initiates with the value
        # the variable gets.
        # For Assignment, the value cannot be updated in the binder.
        #
        # eg: a = a + 2
        # When evaluating, 'a' has a value of 'a + 2' if the value is updated in the binder,
        # which leads to an infinite loop as 'a' keeps trying to find the value of 'a'.

        return self.scope.tryGetVariable(node.varName)[1]

    def evaluateLiteralExpression(self, node):
        return node.value

    def evaluateVariableExpression(self, node):
        success, var = self.scope.tryGetVariable(node.var.name)
        if success:
            return self.evaluateNode(var.value)

        # All non declared variables should be taken care of in the binder
        raise NameError(f"Variable {node.var.name} doesn't exist.")

    def evaluateUnaryExpression(self, node):
        if node.operator.isInstance(TokenTypes.MinusOperator):
            return -(self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.NotOperator):
            return not (self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.PlusPlusOperator):
            self.scope.updateValue(
                node.operand.var.name,
                self.evaluateNode(node.operand) + 1,
                node.operand.text_span,
            )

        if node.operator.isInstance(TokenTypes.MinusMinusOperator):
            self.child.updateValue(
                node.operand.var.name,
                self.evaluateNode(node.operand) - 1,
                node.operand.text_span,
            )

        return self.evaluateNode(node.operand)
