from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import BinaryOperatorNode
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.IfStatement import IfStatement
from syntax_tree.UnaryNode import UnaryOperatorNode

from error.ErrorBag import ErrorBag
from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types
from type_handling.helperFunctions import getBinaryOperatorTypes, getUnaryOperatorTypes

from variables.Variable import getStatsFromDeclarationKeyword
from variables.Scope import Scope

from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundIfCondition import BoundIfCondition
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundUnaryExpression import BoundUnaryExpression


class Binder:
    def __init__(self, root, errorBag, globalScope):
        self.root = root
        self.index = 0
        self.globalScope = globalScope
        self.errorBag = errorBag
        self.currentScope = globalScope

    def bind(self):
        return self.bindExpression(self.root), self.globalScope, self.errorBag

    def bindExpression(self, node):
        if isinstance(node, BlockStatement):
            return self.bindBlockStatement(node)

        if isinstance(node, DeclarationNode):
            return self.bindDeclarationExpression(node)

        if isinstance(node, AssignmentNode):
            return self.bindAssignmentExpression(node)

        if isinstance(node, BinaryOperatorNode):
            return self.bindBinaryExpression(node)

        if isinstance(node, IfStatement):
            return self.bindIfStatement(node)

        if isinstance(node, UnaryOperatorNode):
            return self.bindUnaryExpression(node)

        if isinstance(node, ExpressionNode):
            return self.bindExpressionNode(node)

    def bindBlockStatement(self, node):
        prevScope = self.currentScope
        if node == self.root:
            scope = self.globalScope
        else:
            scope = Scope(prevScope)
            self.currentScope = scope
        lst = []
        for expression in node.getChildren():
            lst.append(self.bindExpression(expression))
        self.currentScope = prevScope
        return BoundBlockStatement(lst, scope, node.text_span)

    def bindDeclarationExpression(self, node):
        varType, isConst = getStatsFromDeclarationKeyword(node.declarationKeyword)
        varName = node.identifier.value
        varValue = self.bindExpression(node.expression)
        if varType == None:
            varType = varValue.type
        if varType != varValue.type:
            self.errorBag.assignmentTypeError(
                varValue.type, varType, varValue.text_span
            )

        if not self.currentScope.tryInitialiseVariable(
            varName, varValue, varType, isConst
        ):
            self.errorBag.initialiseError(varName, node.identifier.text_span)

        return BoundDeclarationExpression(
            node.declarationKeyword, varType, varName, varValue, node.text_span
        )

    def bindAssignmentExpression(self, node):
        varName = node.identifier.value
        varValue = self.bindExpression(node.expression)

        success, var = self.currentScope.tryGetVariable(varName)
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

    def bindBinaryExpression(self, node):
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

    def bindIfStatement(self, node):
        condition = self.bindExpression(node.condition)
        if condition.type != Types.Bool:
            self.errorBag.typeError(condition.type, Types.BOol, condition.text_span)
        thenBlock = self.bindExpression(node.thenBlock)
        if node.elseBlock:
            elseBlock = self.bindExpression(node.elseBlock)
        else:
            elseBlock = None
        return BoundIfCondition(condition, thenBlock, elseBlock, node.text_span)

    def bindUnaryExpression(self, node):
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

        return BoundUnaryExpression(resultType, operator, operand, node.text_span)

    def bindExpressionNode(self, node):
        if node.isInstance(TokenTypes.Variable):
            success, var = self.currentScope.tryGetVariable(node.value)
            if not success:
                self.errorBag.nameError(node.value, node.text_span)
                return BoundLiteralExpression(Types.Unknown, node.value, node.text_span)

            return BoundVariableExpression(var, node.text_span)
        else:
            return BoundLiteralExpression(node.type, node.value, node.text_span)
