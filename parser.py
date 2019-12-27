from lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.DeclarationNode import DeclarationNode
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

    def parse(self, text, errorBag):
        self.errorBag = errorBag
        self.text = text
        self.index = 0
        lexer = Lexer(self.errorBag)
        tokenList, self.errorBag = lexer.lex(text)
        self.tokenList = self.sanitize(tokenList) + [EOF_TOKEN]

        return self.evaluate(), self.errorBag

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
        return DeclarationNode(declarationToken, self.evaluateAssignmentExpression())

    def evaluateAssignmentExpression(self):
        varNode = self.evaluateGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.AssignmentOperator)

        right = self.evaluate()

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

        if cur.isInstance(TokenTypes.Boolean, TokenTypes.Number, TokenTypes.Variable):
            return self.evaluateGeneralExpression(cur.token_type)

    def evaluateParanExpression(self):
        self.match(TokenTypes.OpenParan)
        expression = self.evaluate()
        self.match(TokenTypes.CloseParan)
        return expression

    def evaluateGeneralExpression(self, token_type):
        cur = self.match(token_type)
        return ExpressionNode(cur)
