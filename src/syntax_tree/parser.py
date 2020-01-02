from syntax_tree.lexer import Lexer
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.IfStatement import IfStatement
from syntax_tree.ForStatement import constructForStatement
from syntax_tree.FunctionCallNode import FunctionCallNode
from syntax_tree.FunctionDeclarationNode import FunctionDeclarationNode
from syntax_tree.ReturnStatement import ReturnStatement
from syntax_tree.WhileStatement import WhileStatement
from syntax_tree.UnaryNode import *

from token_handling.Token import *
from token_handling.TokenTypes import *
from variables.Variable import Variable, getStatsFromDeclarationKeyword
from variables.default_functions.InbuiltFunctions import InbuiltFunctions
from error.ErrorBag import ErrorBag


class Parser:
    def __init__(self, errorBag: ErrorBag):
        self.tokenList = []
        self.errorBag = errorBag
        self.index = 0

    def sanitize(self, tokenList):
        for i in range(len(tokenList) - 1, -1, -1):
            if tokenList[i].isInstance(TokenTypes.Bad, TokenTypes.Whitespace):
                tokenList.pop(i)
        return tokenList

    def parse(self, text: str, errorBag: ErrorBag):
        self.errorBag = errorBag
        self.text = text
        self.index = 0
        lexer = Lexer(self.errorBag)
        continueToNextLine, tokenList, self.errorBag = lexer.lex(text)
        self.tokenList = self.sanitize(tokenList) + [EOF_TOKEN]
        if continueToNextLine:
            return continueToNextLine, None, self.errorBag
        return continueToNextLine, self._parse(), self.errorBag

    def peek(self, offset: int):
        if self.index + offset >= len(self.tokenList):
            return self.tokenList[-1]
        return self.tokenList[self.index + offset]

    def cur(self):
        return self.peek(0)

    def match(self, *expectedTokens: list):
        cur = self.cur()
        if not cur.isInstance(*expectedTokens):
            self.errorBag.tokenError(cur, expectedTokens, cur.text_span)
        self.index += 1
        return cur

    def _parse(self, end_token=TokenTypes.EOF):
        lst = []
        while not self.cur().isInstance(end_token):
            if self.cur().isInstance(TokenTypes.OpenBrace):
                self.index += 1
                lst.append(self._parse(TokenTypes.CloseBrace))
            else:
                lst.append(self.parseStatement())

        self.index += 1

        return BlockStatement(lst)

    def parseStatement(self):
        if self.cur().isInstance(TokenTypes.DeclarationKeyword):
            return self.parseDeclareExpression()

        if self.cur().isInstance(TokenTypes.Variable):
            if self.peek(1).isInstance(TokenTypes.AssignmentOperator):
                return self.parseAssignmentExpression()
            elif self.peek(1).isInstance(*CALC_ASSIGN_OPERATORS) and self.peek(
                2
            ).isInstance(TokenTypes.AssignmentOperator):
                return self.parseCalculateAssignmentExpression()

        if self.cur().isInstance(TokenTypes.IfKeyword):
            return self.parseIfStatement()

        if self.cur().isInstance(TokenTypes.WhileKeyword):
            return self.parseWhileStatement()

        if self.cur().isInstance(TokenTypes.ForKeyword):
            return self.parseForStatement()

        if self.cur().isInstance(TokenTypes.ReturnKeyword):
            return self.parseReturnStatement()

        return self.parseBinaryExpression()

    def parseDeclareExpression(self):
        declarationToken = self.match(TokenTypes.DeclarationKeyword)
        if self.peek(1).isInstance(TokenTypes.AssignmentOperator):
            return DeclarationNode(declarationToken, self.parseAssignmentExpression())

        return self.parseFunctionDeclaration(declarationToken)

    def parseAssignmentExpression(self):
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.AssignmentOperator)

        right = self.parseStatement()

        return AssignmentNode(varNode, right, TokenTypes.AssignmentOperator)

    def parseFunctionDeclaration(self, declarationToken: Token):
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.OpenParan)
        params = []
        if not self.cur().isInstance(TokenTypes.CloseParan):
            while not self.cur().isInstance(TokenTypes.EOF):
                token = self.match(TokenTypes.DeclarationKeyword)
                varType = getStatsFromDeclarationKeyword(token.value)[0]
                if varType == None:
                    self.errorBag.tokenError(
                        token.value, "int, bool, float, string", token.text_span
                    )
                var = self.match(TokenTypes.Variable)
                params.append(Variable(var.value, varType))
                if self.cur().isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break

        self.match(TokenTypes.CloseParan)
        self.match(TokenTypes.OpenBrace)

        functionBody = self._parse(TokenTypes.CloseBrace)

        return FunctionDeclarationNode(declarationToken, varNode, params, functionBody)

    def parseCalculateAssignmentExpression(self):
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        operator = self.match(*CALC_ASSIGN_OPERATORS)
        assignment_operator = self.match(TokenTypes.AssignmentOperator)
        right = self.parseStatement()
        newVal = BinaryOperatorNode(varNode, right, operator)
        return AssignmentNode(varNode, newVal, assignment_operator)

    def parseFunctionExpression(self):
        funcToken = self.match(TokenTypes.Variable)
        self.match(TokenTypes.OpenParan)
        params = []
        if not self.cur().isInstance(TokenTypes.CloseParan):
            while not self.cur().isInstance(TokenTypes.EOF):
                params.append(self.parseStatement())
                if self.cur().isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break

        self.match(TokenTypes.CloseParan)

        return FunctionCallNode(funcToken, tuple(params), TokenTypes.Function)

    def parseIfStatement(self):
        ifToken = self.match(TokenTypes.IfKeyword)
        condition = self.parseStatement()
        openBrace = self.match(TokenTypes.OpenBrace)
        thenBlock = self._parse(TokenTypes.CloseBrace)
        elseBlock = None
        if self.cur().isInstance(TokenTypes.ElseKeyword):
            self.index += 1
            if self.cur().isInstance(TokenTypes.IfKeyword):
                elseBlock = self.parseIfStatement()
            else:
                self.match(TokenTypes.OpenBrace)
                elseBlock = self._parse(TokenTypes.CloseBrace)

        return IfStatement(ifToken, condition, thenBlock, elseBlock)

    def parseWhileStatement(self):
        whileToken = self.match(TokenTypes.WhileKeyword)
        condition = self.parseStatement()
        openBrace = self.match(TokenTypes.OpenBrace)
        whileBlock = self._parse(TokenTypes.CloseBrace)

        return WhileStatement(whileToken, condition, whileBlock)

    def parseForStatement(self):
        forToken = self.match(TokenTypes.ForKeyword)
        variable = self.parseGeneralExpression(TokenTypes.Variable)
        inToken = self.match(TokenTypes.InKeyword)
        rangeToken = self.match(TokenTypes.RangeKeyword)
        upperBound = self.parseParanExpression()
        openBrace = self.match(TokenTypes.OpenBrace)
        forBlock = self._parse(TokenTypes.CloseBrace)

        return constructForStatement(variable, upperBound, forBlock)

    def parseReturnStatement(self):
        returnToken = self.match(TokenTypes.ReturnKeyword)
        to_return = self.parseStatement()

        return ReturnStatement(returnToken, to_return)

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

        if cur.isInstance(TokenTypes.Variable) and self.peek(1).isInstance(
            TokenTypes.OpenParan
        ):
            return self.parseFunctionExpression()

        if cur.isInstance(
            TokenTypes.Boolean,
            TokenTypes.Number,
            TokenTypes.Variable,
            TokenTypes.String,
        ):
            return self.parseGeneralExpression(cur.token_type)

        self.errorBag.unexpectedToken(cur, cur.text_span)
        self.index += 1

    def parseParanExpression(self):
        self.match(TokenTypes.OpenParan)
        expression = self.parseStatement()
        self.match(TokenTypes.CloseParan)
        return expression

    def parseFunctionExpression(self):
        funcToken = self.match(TokenTypes.Variable)
        if funcToken.value == "print":
            funcType = InbuiltFunctions.Print
        elif funcToken.value == "input":
            funcType = InbuiltFunctions.Input
        elif funcToken.value == "random":
            funcType = InbuiltFunctions.Random
        else:
            funcType = InbuiltFunctions.Regular
        self.match(TokenTypes.OpenParan)
        params = []
        if not self.cur().isInstance(TokenTypes.CloseParan):
            while not self.cur().isInstance(TokenTypes.EOF):
                params.append(self.parseStatement())
                if self.cur().isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break

        self.match(TokenTypes.CloseParan)

        return FunctionCallNode(funcToken, params, TokenTypes.Function, funcType)

    def parseGeneralExpression(self, token_type: TokenTypes):
        cur = self.match(token_type)
        return ExpressionNode(cur)
