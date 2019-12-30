from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import BinaryOperatorNode
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.FunctionDeclarationNode import FunctionDeclarationNode
from syntax_tree.FunctionNode import FunctionNode
from syntax_tree.IfStatement import IfStatement
from syntax_tree.ReturnStatement import ReturnStatement
from syntax_tree.WhileStatement import WhileStatement
from syntax_tree.UnaryNode import UnaryOperatorNode

from error.ErrorBag import ErrorBag
from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types
from type_handling.helperFunctions import (
    getUnaryOperatorTypes,
    checkBinaryType,
    getType,
)

from variables.Variable import getStatsFromDeclarationKeyword
from variables.Scope import Scope
from variables.FunctionVariable import FunctionVariable

from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundIfStatement import BoundIfStatement
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundReturnStatement import BoundReturnStatement
from binder.BoundUnaryExpression import BoundUnaryExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundWhileStatement import BoundWhileStatement


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

        if isinstance(node, ExpressionNode):
            return self.bindExpressionNode(node)

        if isinstance(node, FunctionDeclarationNode):
            return self.bindFunctionDeclaration(node)

        if isinstance(node, FunctionNode):
            return self.bindFunctionCall(node)

        if isinstance(node, IfStatement):
            return self.bindIfStatement(node)

        if isinstance(node, ReturnStatement):
            return self.bindReturnStatement(node)

        if isinstance(node, WhileStatement):
            return self.bindWhileStatement(node)

        if isinstance(node, UnaryOperatorNode):
            return self.bindUnaryExpression(node)

    def bindBlockStatement(
        self, node, block_type=Types.Unknown, variables={}, functional=False
    ):
        prevScope = self.currentScope
        if node == self.root:
            scope = self.globalScope
        else:
            scope = Scope(variables, prevScope)
            self.currentScope = scope
        lst = []
        for expression in node.getChildren():
            lst.append(self.bindExpression(expression))
        self.currentScope = prevScope
        return BoundBlockStatement(lst, scope, block_type, node.text_span, functional)

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

        resultType, self.errorBag = checkBinaryType(
            operator, left, right, self.errorBag
        )

        return BoundBinaryExpression(resultType, left, operator, right, node.text_span)

    def bindExpressionNode(self, node):
        if node.isInstance(TokenTypes.Variable):
            success, var = self.currentScope.tryGetVariable(node.value)
            if not success:
                self.errorBag.nameError(node.value, node.text_span)
                return BoundLiteralExpression(Types.Unknown, node.value, node.text_span)

            return BoundVariableExpression(var, node.text_span)
        else:
            return BoundLiteralExpression(
                getType(node.value), node.value, node.text_span
            )

    def bindFunctionDeclaration(self, node):
        varType, _ = getStatsFromDeclarationKeyword(node.declarationKeyword)
        varName = node.identifier.value
        varValue = FunctionVariable(
            varName, varType, node.params, node.functionBody, node.text_span
        )

        if not self.currentScope.tryInitialiseVariable(
            varName, varValue, varType, True
        ):
            self.errorBag.initialiseError(varName, node.identifier.text_span)

        return BoundDeclarationExpression(
            node.declarationKeyword, varType, varName, varValue, node.text_span
        )

    def bindFunctionCall(self, node):
        success, var = self.currentScope.tryGetVariable(node.name)
        func = var.value
        if not success:
            self.errorBag.nameError(node.name, node.text_span)
            return BoundLiteralExpression(Types.Unknown, node.name, node.text_span)

        if len(node.params) != len(func.params):
            self.errorBag.numParamError(
                node.name, len(node.params), len(func.params), node.text_span
            )

        params = {}
        for i in range(len(node.params)):
            paramVar = func.params[i]
            param = self.bindExpression(node.params[i])
            if param.type != func.params[i].type:
                self.errorBag.typeError(
                    param.type, func.params[i].type, param.text_span
                )
            paramVar.value = param
            params[paramVar.name] = paramVar

        return self.bindBlockStatement(func.functionBody, func.type, params, True)

    def bindIfStatement(self, node):
        condition = self.bindExpression(node.condition)
        if condition.type != Types.Bool:
            self.errorBag.typeError(condition.type, Types.Bool, condition.text_span)
        thenBlock = self.bindExpression(node.thenBlock)
        if node.elseBlock:
            elseBlock = self.bindExpression(node.elseBlock)
        else:
            elseBlock = None
        return BoundIfStatement(condition, thenBlock, elseBlock, node.text_span)

    def bindReturnStatement(self, node):
        to_return = self.bindExpression(node.to_return)
        return BoundReturnStatement(to_return, node.text_span)

    def bindWhileStatement(self, node):
        condition = self.bindExpression(node.condition)
        if condition.type != Types.Bool:
            self.errorBag.typeError(condition.type, Types.Bool, condition.text_span)
        whileBlock = self.bindExpression(node.whileBlock)

        return BoundWhileStatement(condition, whileBlock, node.text_span)

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
