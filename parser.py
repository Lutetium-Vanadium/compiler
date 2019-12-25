from lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.UnaryNode import *
from token_handling.Token import *
from token_handling.TokenTypes import *


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
        lexer = Lexer(self.errorBag)
        # TODO remove EOL_TOKEN at end, should be put manually when language is complete
        self.tokenList = self.sanitize(lexer.lex(text)) + [EOL_TOKEN]

        return self.variables, self.evaluate(self.tokenList)[0]

    def peek(self, offSet):
        return self.tokenList[self.index + offSet]

    def cur(self):
        return self.peek(0)

    def evaluate(self):
        if self.cur().isInstance(TokenTypes.Variable) and self.peek(1).isInstance(
            TokenTypes.AssignmentOperator
        ):
            self.evaluateAssignmentExpression()

        self.evaluateBinaryExpression()

    def evaluateAssignmentExpression(self):
        var = self.cur()
        self.index += 2
        right = self.evaluate()
        self.variables[var] = right
        return AssignmentNode(var, right)

    def evaluateBinaryExpression(self, parentPrecedence=0):
        unaryPrecedence = getUnaryPrecedence(self.cur())
        if unaryPrecedence != 0 and unaryPrecedence >= parentPrecedence:
            operator = self.cur()
            self.index += 1
            operand = self.evaluateBinaryExpression(unaryPrecedence)
            left = UnaryOperatorNode(operand, operator)
        else:
            left = self.evaluatePrimaryExpression()

    def evaluatePrimaryExpression(self):
        cur = self.cur()

        if cur.isInstance(TokenTypes.OpenParan):
            return self.evaluateParanExpression()

        if cur.isInstance(TokenTypes.Boolean):
            return self.evaluateBooleanExpression()

        if cur.isInstance(TokenTypes.Number):
            return self.evaluateNumberExpression()

        if cur.isInstance(TokenTypes.Variable):
            return self.evaluateVariableExpression()

    def evaluateParanExpression(self):
        self.index += 1
        expression = self.evaluate()
        self.index += 1
        return expression
