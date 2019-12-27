from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import BinaryOperatorNode
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.UnaryNode import UnaryOperatorNode

from error.ErrorBag import ErrorBag
from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types
from type_handling.helperFunctions import getBinaryOperatorTypes

from variables.Variable import getStatsFromDeclarationKeyword
from variables.VariableBag import VariableBag

from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundUnaryExpression import BoundUnaryExpression


class Binder:
    def __init__(self, root, errorBag, variables):
        self.root = root
        self.index = 0
        self.variables = variables
        self.errorBag = errorBag

    def bind(self):
        return self.bindExpression(self.root), self.variables, self.errorBag

    def bindExpression(self, node):
        if isinstance(node, DeclarationNode):
            return self.bindDeclarationExpression(node)

        if isinstance(node, AssignmentNode):
            return self.bindAssignmentExpression(node)

        if isinstance(node, BinaryOperatorNode):
            return self.bindBinaryExpression(node)

        if isinstance(node, UnaryOperatorNode):
            return self.bindUnaryExpression(node)

        if isinstance(node, ExpressionNode):
            return self.bindExpressionNode(node)

    def bindDeclarationExpression(self, node: DeclarationNode):
        varType, isConst = getStatsFromDeclarationKeyword(node.declarationKeyword)
        varName = node.identifier.value
        varValue = self.bindExpression(node.expression)
        if varType == None:
            varType = varValue.type
        if varType != varValue.type:
            self.errorBag.assignmentTypeError(
                varValue.type, varType, varValue.text_span
            )

        if not self.variables.tryInitialiseVariable(
            varName, varValue, varType, isConst
        ):
            self.errorBag.initialiseError(varName, node.identifier.text_span)

        return BoundDeclarationExpression(
            node.declarationKeyword, varType, varName, varValue, node.text_span
        )

    def bindAssignmentExpression(self, node: AssignmentNode):
        varName = node.identifier.value
        varValue = self.bindExpression(node.expression)

        success, var = self.variables.tryGetVariable(varName)
        if not success:
            self.errorBag.nameError(varName, node.identifier.text_span)
            varType = None
        else:
            if var.isConst:
                self.errorBag.reassignConstError(varName, node.identifier.text_span)
            if var.type != varValue.type:
                self.errorBag.typeError(varValue.type, var.type, varValue.text_span)
            varType = var.type

        return BoundAssignmentExpression(varType, varName, varValue, node.text_span)

    def bindBinaryExpression(self, node: BinaryOperatorNode):
        left = self.bindExpression(node.left)
        operator = node.operatorToken
        right = self.bindExpression(node.right)
        operandType, resultType = getBinaryOperatorTypes(operator)

        if operandType == Types.Int and (
            left.type == Types.Float or right.type == Types.Float
        ):
            if resultType == Types.Int:
                resultType = Types.Float
            operandType = Types.Float

        if (
            left.type != operandType
            and operandType == Types.Float
            and left.type != Types.Int
        ):
            self.errorBag.typeError(left.type, operandType, left.text_span)

        if (
            right.type != operandType
            and operandType == Types.Float
            and right.type != Types.Int
        ):
            self.errorBag.typeError(right.type, operandType, right.text_span)

        return BoundBinaryExpression(resultType, left, operator, right, node.text_span)

    def bindUnaryExpression(self, node: UnaryOperatorNode):
        operator = node.operatorToken
        operand = self.bindExpression(node.child)
        operandType, resultType = getUnaryOperatorTypes(operator)

        if operator.isInstance(
            TokenTypes.PlusPlusOperator, TokenTypes.MinusMinusOperator
        ) and not isinstance(operand, BoundVariableExpression):
            self.errorBag.syntaxError(
                operand.getName(),
                operand.text_span,
                f"Unary Operator {operator.token_type} requires a variable as operand",
            )

        if operand.type != operandType:
            self.errorBag.typeError(operand.type, operandType, operand.text_span)

        return BoundBinaryExpression(resultType, operator, operand, node.text_span)

    def bindExpressionNode(self, node: ExpressionNode):
        if node.isInstance(TokenTypes.Variable):
            success, var = self.variables.tryGetVariable(node.value)
            if not success:
                self.errorBag.nameError(node.value, node.text_span)
                return BoundLiteralExpression(Types.Unknown, node.value, node.text_span)

            return BoundVariableExpression(var, node.text_span)
        else:
            return BoundLiteralExpression(node.type, node.value, node.text_span)
