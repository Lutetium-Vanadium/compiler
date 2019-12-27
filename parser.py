from lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
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

    def parse(self, text, errorBag):
        self.errorBag = errorBag
        self.text = text
        self.index = 0
        lexer = Lexer(self.errorBag)
        tokenList, self.errorBag = lexer.lex(text)
        self.tokenList = self.sanitize(tokenList) + [EOF_TOKEN]

        return self._parse(), self.errorBag

    def peek(self, offSet):
        return self.tokenList[self.index + offSet]

    def cur(self):
        return self.peek(0)

    def match(self, *expectedTokens):
        cur = self.cur()
        if not cur.isInstance(*expectedTokens):
            self.errorBag.tokenError(cur, expectedTokens, cur.text_span)
        self.index += 1
        return cur

    def _parse(self):
        if self.cur().isInstance(TokenTypes.DeclarationKeyword):
            return self.parseDeclareExpression()

        if self.cur().isInstance(TokenTypes.Variable):
            if self.peek(1).isInstance(TokenTypes.AssignmentOperator):
                return self.parseAssignmentExpression()
            elif self.peek(1).isInstance(*CALC_ASSIGN_OPERATORS) and self.peek(2).isInstance(TokenTypes.AssignmentOperator):
                return self.parseCalculateAssignmentExpression()

        return self.parseBinaryExpression()

    def parseDeclareExpression(self):
        declarationToken = self.match(TokenTypes.DeclarationKeyword)
        return DeclarationNode(declarationToken, self.parseAssignmentExpression())

    def parseAssignmentExpression(self):
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.AssignmentOperator)

        right = self._parse()

        return AssignmentNode(varNode, right, TokenTypes.AssignmentOperator)
    
    def parseCalculateAssignmentExpression(self):
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        operator = self.match(*CALC_ASSIGN_OPERATORS)
        assignment_operator = self.match(TokenTypes.AssignmentOperator)
        right = self._parse()
        newVal = BinaryOperatorNode(varNode, right, operator)
        return AssignmentNode(varNode, newVal, assignment_operator)

    def parseBinaryExpression(self, parentPrecedence=0):
        unaryPrecedence = getUnaryPrecedence(self.cur())
        if unaryPrecedence != 0 and unaryPrecedence >= parentPrecedence:
            operator = self.cur()
            self.index += 1
            operand = self.parseBinaryExpression(unaryPrecedence)
            left = UnaryOperatorNode(operand, operator)
        else:
            left = self.parsePrimaryExpression()

        while True:
            precedence = getBinaryPrecedence(self.cur())
            if precedence == 0 or precedence <= parentPrecedence:
                break

            operatorToken = self.cur()
            self.index += 1
            right = self.parseBinaryExpression(precedence)
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

    def parsePrimaryExpression(self):
        cur = self.cur()

        if cur.isInstance(TokenTypes.OpenParan):
            return self.parseParanExpression()

        if cur.isInstance(TokenTypes.Boolean, TokenTypes.Number, TokenTypes.Variable):
            return self.parseGeneralExpression(cur.token_type)

    def parseParanExpression(self):
        self.match(TokenTypes.OpenParan)
        expression = self._parse()
        self.match(TokenTypes.CloseParan)
        return expression

    def parseGeneralExpression(self, token_type):
        cur = self.match(token_type)
        return ExpressionNode(cur)
