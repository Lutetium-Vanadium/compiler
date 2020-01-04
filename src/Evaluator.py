from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundFunctionCall import BoundFunctionCall
from binder.BoundIfStatement import BoundIfStatement
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundNode import BoundNode
from binder.BoundReturnStatement import BoundReturnStatement
from binder.BoundUnaryExpression import BoundUnaryExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundWhileStatement import BoundWhileStatement

from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types
from variables.default_functions.InbuiltFunctions import InbuiltFunctions

from random import random


class Evaluator:
    def evaluate(self, syntaxTree: BoundBlockStatement):
        self.syntaxTree = syntaxTree
        self.scope = None
        self.returnFromBlock = False
        return self.evaluateNode(self.syntaxTree)

    def evaluateNode(self, node: BoundNode):
        if isinstance(node, BoundDeclarationExpression):
            return self.evaluateDeclarationExpression(node)

        if isinstance(node, BoundBlockStatement):
            return self.evaluateBlockStatement(node)

        if isinstance(node, BoundDeclarationExpression):
            return self.evaluateDeclarationExpression(node)

        if isinstance(node, BoundAssignmentExpression):
            return self.evaluateAssignmentExpression(node)

        if isinstance(node, BoundBinaryExpression):
            return self.evaluateBinaryExpression(node)

        if isinstance(node, BoundFunctionCall):
            return self.evaluateFunctionCall(node)

        if isinstance(node, BoundIfStatement):
            return self.evaluateIfCondition(node)

        if isinstance(node, BoundLiteralExpression):
            return self.evaluateLiteralExpression(node)

        if isinstance(node, BoundReturnStatement):
            return self.evaluateReturnStatement(node)

        if isinstance(node, BoundVariableExpression):
            return self.evaluateVariableExpression(node)

        if isinstance(node, BoundWhileStatement):
            return self.evaluateWhileStatement(node)

        if isinstance(node, BoundUnaryExpression):
            return self.evaluateUnaryExpression(node)

    def evaluateBlockStatement(self, node: BoundBlockStatement):
        prevScope = self.scope
        self.scope = node.scope
        value = None
        for boundExpression in node.children:
            value = self.evaluateNode(boundExpression)
            if self.returnFromBlock:
                if node.isFunction:
                    self.returnFromBlock = False
                break
        self.scope = prevScope
        return value

    def evaluateAssignmentExpression(self, node: BoundAssignmentExpression):
        self.scope.updateValue(
            node.varName, self.evaluateNode(node.varValue), node.varValue.text_span
        )
        return self.scope.tryGetVariable(node.varName)[1]

    def evaluateBinaryExpression(self, node: BoundBinaryExpression):
        # Arithmetic Operators
        if node.operator.isInstance(TokenTypes.PlusOperator):
            if node.type == Types.String:
                return str(self.evaluateNode(node.left)) + str(
                    self.evaluateNode(node.right)
                )
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
        # For Declaration, value need not be updated as the binder initiates with the value
        # the variable gets.
        # For Assignment, the value cannot be updated in the binder.
        #
        # eg: a = a + 2
        # When evaluating, 'a' has a value of 'a + 2' if the value is updated in the binder,
        # which leads to an infinite loop as 'a' keeps trying to find the value of 'a'.

        return self.scope.tryGetVariable(node.varName)[1]

    def evaluateFunctionCall(self, node: BoundFunctionCall):
        success, func = self.scope.tryGetVariable(node.name)
        if not success:
            # All non declared variables should be taken care of in the binder
            raise NameError(f"Variable {node.name} doesn't exist.")

        params = []
        for i in range(len(func.params)):
            param = func.params[i].copy()
            value = self.evaluateNode(node.paramValues[i])
            param.value = BoundLiteralExpression(
                Types.Int, value, node.paramValues[i].text_span, type(value) == list
            )
            params.append(param)

        if node.function_type == InbuiltFunctions.Input:
            return input()
        if node.function_type == InbuiltFunctions.Random:
            return random()
        if node.function_type == InbuiltFunctions.Print:
            print(*params)
        else:
            functionBody = func.functionBody.copy()
            functionBody.addVariables(params)

            return self.evaluateNode(functionBody)

    def evaluateIfCondition(self, node: BoundIfStatement):
        isTrue = self.evaluateNode(node.condition)
        if isTrue:
            return self.evaluateNode(node.thenBlock)
        elif node.elseBlock:
            return self.evaluateNode(node.elseBlock)

    def evaluateLiteralExpression(self, node: BoundLiteralExpression):
        if node.isList:
            return [self.evaluateNode(item) for item in node.value]
        return node.value

    def evaluateReturnStatement(self, node: BoundReturnStatement):
        returnVal = self.evaluateNode(node.to_return)
        self.returnFromBlock = True
        return returnVal

    def evaluateVariableExpression(self, node: BoundVariableExpression):
        success, var = self.scope.tryGetVariable(node.name)
        if not success:
            # All non declared variables should be taken care of in the binder
            raise NameError(f"Variable {node.name} doesn't exist.")

        return self.evaluateNode(var.value)

    def evaluateWhileStatement(self, node: BoundWhileStatement):
        value = None
        while self.evaluateNode(node.condition):
            value = self.evaluateNode(node.whileBlock)
        return value

    def evaluateUnaryExpression(self, node: BoundUnaryExpression):
        if node.operator.isInstance(TokenTypes.MinusOperator):
            return -(self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.NotOperator):
            return not (self.evaluateNode(node.operand))

        if node.operator.isInstance(TokenTypes.PlusPlusOperator):
            self.scope.updateValue(
                node.operand.name,
                self.evaluateNode(node.operand) + 1,
                node.operand.text_span,
            )

        if node.operator.isInstance(TokenTypes.MinusMinusOperator):
            self.scope.updateValue(
                node.operand.name,
                self.evaluateNode(node.operand) - 1,
                node.operand.text_span,
            )

        return self.evaluateNode(node.operand)
