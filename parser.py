from lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.UnaryNode import *
from token_handling.Token import *
from token_handling.TokenTypes import *
from variables.Variable import *


class Parser:
    def __init__(self, errorBag):
        self.tokenList = []
        self.errorBag = errorBag
        self.index = 0

    def sanitize(self, tokenList):
        for i in range(len(tokenList) - 1, -1, -1):
            if tokenList[i].isInstance(TokenTypes.Bad, TokenTypes.Whitespace):
                tokenList.pop(i)
        return tokenList

    def parse(self, text, variables):
        self.text = text
        self.variables = variables
        self.index = 0
        lexer = Lexer(self.errorBag)
        tokenList, errorBag = lexer.lex(text)
        self.errorBag.extend(errorBag)
        self.tokenList = self.sanitize(tokenList) + [EOF_TOKEN]

        a = self.evaluate()

        return self.variables, a

    def peek(self, offSet):
        return self.tokenList[self.index + offSet]

    def cur(self):
        return self.peek(0)

    def match(self, expectedToken):
        cur = self.cur()
        if not cur.isInstance(expectedToken):
            self.errorBag.tokenError(cur, expectedToken, cur.text_span)
        self.index += 1
        return cur

    def evaluate(self):
        if self.cur().isInstance(TokenTypes.DeclarationKeyword):
            return self.evaluateDeclareExpression()

        if self.cur().isInstance(TokenTypes.Variable) and self.peek(1).isInstance(
            TokenTypes.AssignmentOperator
        ):
            return self.evaluateAssignmentExpression()

        return self.evaluateBinaryExpression()

    def evaluateDeclareExpression(self):
        declarationToken = self.match(TokenTypes.DeclarationKeyword)

        name = self.cur().token_value.value
        data_type, isConst = getStatsFromDeclarationToken(declarationToken)
        var = Variable(name, data_type=data_type, isConst=isConst)

        self.variables[name] = var

        return self.evaluateAssignmentExpression()

    def evaluateAssignmentExpression(self):
        varNode, variableExists = self.evaluateVariableExpression()
        self.match(TokenTypes.AssignmentOperator)

        right = self.evaluate()
        if variableExists and not self.variables[varNode.value.name].trySetValue(
            right.evaluate()
        ):
            self.errorBag.reassignConstError(varNode.value.name, varNode.text_span)

        return AssignmentNode(varNode, right, TokenTypes.AssignmentOperator)

    def evaluateBinaryExpression(self, parentPrecedence=0):
        unaryPrecedence = getUnaryPrecedence(self.cur())
        if unaryPrecedence != 0 and unaryPrecedence >= parentPrecedence:
            operator = self.cur()
            self.index += 1
            operand = self.evaluateBinaryExpression(unaryPrecedence)
            left = UnaryOperatorNode(operand, operator)
        else:
            left = self.evaluatePrimaryExpression()

        while True:
            precedence = getBinaryPrecedence(self.cur())
            if precedence == 0 or precedence <= parentPrecedence:
                break

            operatorToken = self.cur()
            self.index += 1
            right = self.evaluateBinaryExpression(precedence)
            left = BinaryOperatorNode(left, right, operatorToken)

        if self.cur().isInstance(TokenTypes.PlusPlusOperator) and self.peek(
            -1
        ).isInstance(TokenTypes.Variable):
            left.updateValue(+1)
        elif self.cur().isInstance(TokenTypes.MinusMinusOperator) and self.peek(
            -1
        ).isInstance(TokenTypes.Variable):
            left.updateValue(-1)

        return left

    def evaluatePrimaryExpression(self):
        cur = self.cur()

        if cur.isInstance(TokenTypes.OpenParan):
            return self.evaluateParanExpression()

        if cur.isInstance(TokenTypes.Variable):
            return self.evaluateVariableExpression()[0]

        if cur.isInstance(TokenTypes.Boolean, TokenTypes.Number):
            return self.evaluateGeneralExpression(cur.token_type)

    def evaluateParanExpression(self):
        self.match(TokenTypes.OpenParan)
        expression = self.evaluate()
        self.match(TokenTypes.CloseParan)
        return expression

    def evaluateVariableExpression(self):
        cur = self.match(TokenTypes.Variable)
        name = cur.token_value.value
        var = self.variables.get(name)
        if not var:
            self.errorBag.nameError(name, cur.text_span)
        return ExpressionNode(cur, var), var != None

    def evaluateGeneralExpression(self, token_type):
        cur = self.match(token_type)
        return ExpressionNode(cur)
