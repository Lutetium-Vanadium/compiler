from lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.UnaryNode import *
from token_handling.Token import *
from token_handling.TokenTypes import *
from variables.Variable import Variable


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
        # TODO remove EOL_TOKEN at end, should be put manually when language is complete
        self.tokenList = self.sanitize(lexer.lex(text)) + [EOL_TOKEN]

        return self.variables, self.evaluate()

    def peek(self, offSet):
        return self.tokenList[self.index + offSet]

    def cur(self):
        return self.peek(0)

    def evaluate(self):
        if self.cur().isInstance(TokenTypes.Variable) and self.peek(1).isInstance(
            TokenTypes.AssignmentOperator
        ):
            return self.evaluateAssignmentExpression()

        return self.evaluateBinaryExpression()

    def evaluateAssignmentExpression(self):
        varNode = self.evaluateVariableExpression()
        self.index += 1
        right = self.evaluate()
        self.variables[varNode.value.name].value = right.evaluate()
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

        return left

    def evaluatePrimaryExpression(self):
        cur = self.cur()

        if cur.isInstance(TokenTypes.OpenParan):
            return self.evaluateParanExpression()

        if cur.isInstance(TokenTypes.Variable):
            return self.evaluateVariableExpression()

        if cur.isInstance(TokenTypes.Boolean, TokenTypes.Number):
            return self.evaluateGeneralExpression()

    def evaluateParanExpression(self):
        self.index += 1
        expression = self.evaluate()
        self.index += 1
        return expression

    def evaluateVariableExpression(self):
        cur: Token = self.cur()
        self.index += 1
        name = cur.token_value.value
        var = self.variables.get(name)
        if not var:
            var = Variable(name)
            self.variables[name] = var

        return ExpressionNode(cur, var)

    def evaluateGeneralExpression(self):
        cur = self.cur()
        self.index += 1
        return ExpressionNode(cur, cur.token_value.value)
