from syntax_tree.lexer import Lexer
from syntax_tree.Node import Node
from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import *
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.IfStatement import IfStatement
from syntax_tree.ImportStatement import ImportStatement
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
from pointers import ptrVal, pointer
from error.ErrorBag import ErrorBag


class Parser:
    def __init__(self, errorBagPtr: pointer):
        self.tokenList = []
        self._errorBagPtr = errorBagPtr
        self.index = 0

    @property
    def cur(self) -> Token:
        return self.peek(0)

    @property
    def errorBag(self) -> ErrorBag:
        return ptrVal(self._errorBagPtr)

    def sanitize(self, tokenList) -> list:
        for i in range(len(tokenList) - 1, -1, -1):
            if tokenList[i].isInstance(TokenTypes.Bad, TokenTypes.Whitespace):
                tokenList.pop(i)
        return tokenList

    def parse(self, tokenList) -> BlockStatement:
        self.index = 0
        self.tokenList = self.sanitize(tokenList) + [EOF_TOKEN]
        return self._parse()

    def peek(self, offset: int) -> Token:
        if self.index + offset >= len(self.tokenList):
            return self.tokenList[-1]
        return self.tokenList[self.index + offset]

    def match(self, *expectedTokens: list) -> Token:
        cur = self.cur
        if not cur.isInstance(*expectedTokens):
            if len(expectedTokens) == 1:
                expectedTokens = expectedTokens[0]
            self.errorBag.tokenError(cur, expectedTokens, cur.text_span)
        self.index += 1
        return cur

    def _parse(self, end_token=TokenTypes.EOF) -> BlockStatement:
        lst = []
        while not self.cur.isInstance(end_token):
            if self.cur.isInstance(TokenTypes.EOF):
                # Mismatched paranthesis since end_token is not expected to be EOF
                self.errorBag.unexpectedEOF(end_token)
                break 
            if self.cur.isInstance(TokenTypes.OpenBrace):
                self.index += 1
                lst.append(self._parse(TokenTypes.CloseBrace))
            else:
                lst.append(self.parseStatement())

        self.index += 1

        return BlockStatement(lst)

    def parseStatement(self,) -> Node:
        if self.cur.isInstance(TokenTypes.DeclarationKeyword):
            return self.parseDeclareExpression()

        if self.cur.isInstance(TokenTypes.Variable):
            if self.peek(1).isInstance(TokenTypes.AssignmentOperator):
                return self.parseAssignmentExpression()
            elif self.peek(1).isInstance(*CALC_ASSIGN_OPERATORS) and self.peek(2).isInstance(TokenTypes.AssignmentOperator):
                return self.parseCalculateAssignmentExpression()

        if self.cur.isInstance(TokenTypes.ImportKeyword):
            return self.parseImportStatement()

        if self.cur.isInstance(TokenTypes.IfKeyword):
            return self.parseIfStatement()

        if self.cur.isInstance(TokenTypes.WhileKeyword):
            return self.parseWhileStatement()

        if self.cur.isInstance(TokenTypes.ForKeyword):
            return self.parseForStatement()

        if self.cur.isInstance(TokenTypes.ReturnKeyword):
            return self.parseReturnStatement()

        return self.parseBinaryExpression()

    def parseDeclareExpression(self) -> Node:
        declarationToken = self.match(TokenTypes.DeclarationKeyword)
        if declarationToken.value == "list":
            start = self.match(TokenTypes.LTOperator)
            subtype = self.match(TokenTypes.DeclarationKeyword)
            if subtype.value in ["const", "var"]:
                self.errorBag.unexpectedToken(subtype, subtype.text_span)
            end = self.match(TokenTypes.GTOperator)

            value = f"{declarationToken.value}<{subtype.value}>"

            declarationToken = Token(value, TokenTypes.List, declarationToken.text_span.start)


        if self.peek(1).isInstance(TokenTypes.OpenParan):
            return self.parseFunctionDeclaration(declarationToken)

        varNode = self.parseGeneralExpression(TokenTypes.Variable)

        if self.cur.isInstance(TokenTypes.AssignmentOperator):
            self.index += 1

            right = self.parseStatement()
            return DeclarationNode(declarationToken, varNode, right, TokenTypes.AssignmentOperator)

        return DeclarationNode(
            declarationToken,
            varNode,
            ExpressionNode(None, TextSpan(-1, 0)),
            TokenTypes.AssignmentOperator,
        )

    def parseAssignmentExpression(self) -> AssignmentNode:
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.AssignmentOperator)

        right = self.parseStatement()

        return AssignmentNode(varNode, right, TokenTypes.AssignmentOperator)

    def parseFunctionDeclaration(
        self, declarationToken: Token
    ) -> FunctionDeclarationNode:
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        self.match(TokenTypes.OpenParan)
        params = []
        if not self.cur.isInstance(TokenTypes.CloseParan):
            while not self.cur.isInstance(TokenTypes.EOF):
                token = self.match(TokenTypes.DeclarationKeyword)
                varType = getStatsFromDeclarationKeyword(token.value)[0]
                if varType == None:
                    self.errorBag.tokenError(
                        token.value, "int, bool, float, string", token.text_span
                    )
                var = self.match(TokenTypes.Variable)
                params.append(Variable(var.value, varType))
                if self.cur.isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break

        self.match(TokenTypes.CloseParan)
        self.match(TokenTypes.OpenBrace)

        functionBody = self._parse(TokenTypes.CloseBrace)

        return FunctionDeclarationNode(declarationToken, varNode, params, functionBody)

    def parseCalculateAssignmentExpression(self) -> AssignmentNode:
        varNode = self.parseGeneralExpression(TokenTypes.Variable)
        operator = self.match(*CALC_ASSIGN_OPERATORS)
        assignment_operator = self.match(TokenTypes.AssignmentOperator)
        right = self.parseStatement()
        newVal = BinaryOperatorNode(varNode, right, operator)
        return AssignmentNode(varNode, newVal, assignment_operator)

    def parseImportStatement(self) -> ImportStatement:
        importToken = self.match(TokenTypes.ImportKeyword)
        filePath = self.parseGeneralExpression(TokenTypes.String)

        return ImportStatement(importToken, filePath)

    def parseIfStatement(self) -> IfStatement:
        ifToken = self.match(TokenTypes.IfKeyword)
        condition = self.parseStatement()
        openBrace = self.match(TokenTypes.OpenBrace)
        thenBlock = self._parse(TokenTypes.CloseBrace)
        elseBlock = None
        if self.cur.isInstance(TokenTypes.ElseKeyword):
            self.index += 1
            if self.cur.isInstance(TokenTypes.IfKeyword):
                elseBlock = self.parseIfStatement()
            else:
                self.match(TokenTypes.OpenBrace)
                elseBlock = self._parse(TokenTypes.CloseBrace)

        return IfStatement(ifToken, condition, thenBlock, elseBlock)

    def parseWhileStatement(self) -> WhileStatement:
        whileToken = self.match(TokenTypes.WhileKeyword)
        condition = self.parseStatement()
        openBrace = self.match(TokenTypes.OpenBrace)
        whileBlock = self._parse(TokenTypes.CloseBrace)

        return WhileStatement(whileToken, condition, whileBlock)

    def parseForStatement(self) -> WhileStatement:
        forToken = self.match(TokenTypes.ForKeyword)
        variable = self.parseGeneralExpression(TokenTypes.Variable)
        inToken = self.match(TokenTypes.InKeyword)
        rangeToken = self.match(TokenTypes.RangeKeyword)
        upperBound = self.parseParanExpression()
        openBrace = self.match(TokenTypes.OpenBrace)
        forBlock = self._parse(TokenTypes.CloseBrace)

        return constructForStatement(variable, upperBound, forBlock)

    def parseReturnStatement(self) -> ReturnStatement:
        returnToken = self.match(TokenTypes.ReturnKeyword)
        to_return = self.parseStatement()

        return ReturnStatement(returnToken, to_return)

    def parseBinaryExpression(self, parentPrecedence=0) -> Node:
        unaryPrecedence = getUnaryPrecedence(self.cur)
        if unaryPrecedence != 0 and unaryPrecedence >= parentPrecedence:
            operator = self.cur
            self.index += 1
            operand = self.parseBinaryExpression(unaryPrecedence)
            left = UnaryOperatorNode(operand, operator)
        else:
            left = self.parsePrimaryExpression()

        while True:
            precedence = getBinaryPrecedence(self.cur)
            if precedence == 0 or precedence <= parentPrecedence:
                break

            operatorToken = self.cur
            self.index += 1
            right = self.parseBinaryExpression(precedence)
            left = BinaryOperatorNode(left, right, operatorToken)
            

        return left

    def parsePrimaryExpression(self,) -> Node:
        if self.cur.isInstance(TokenTypes.OpenParan):
            return self.parseParanExpression()

        if self.cur.isInstance(TokenTypes.OpenBracket):
            return self.parseListExpression()

        if self.cur.isInstance(TokenTypes.Variable) and self.peek(1).isInstance(
            TokenTypes.OpenParan
        ):
            return self.parseFunctionExpression()

        if self.cur.isInstance(
            TokenTypes.Boolean,
            TokenTypes.Number,
            TokenTypes.Variable,
            TokenTypes.String,
        ):
            return self.parseGeneralExpression(self.cur.token_type)

        self.errorBag.unexpectedToken(self.cur, self.cur.text_span)
        self.index += 1

    def parseParanExpression(self,) -> Node:
        self.match(TokenTypes.OpenParan)
        expression = self.parseStatement()
        self.match(TokenTypes.CloseParan)
        return expression

    def parseListExpression(self) -> ExpressionNode:
        start = self.match(TokenTypes.OpenBracket).text_span.start

        items = []
        if not self.cur.isInstance(TokenTypes.CloseBracket):
            while not self.cur.isInstance(TokenTypes.EOF):
                items.append(self.parseBinaryExpression())
                if self.cur.isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break
        end = self.match(TokenTypes.CloseBracket).text_span.end
        text_span = TextSpan(start, end - start)
        return ExpressionNode(items, text_span, TokenTypes.List, True)

    def parseFunctionExpression(self) -> FunctionCallNode:
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
        if not self.cur.isInstance(TokenTypes.CloseParan):
            while not self.cur.isInstance(TokenTypes.EOF):
                params.append(self.parseStatement())
                if self.cur.isInstance(TokenTypes.CommaToken):
                    self.index += 1
                else:
                    break

        self.match(TokenTypes.CloseParan)

        return FunctionCallNode(funcToken, params, TokenTypes.Function, funcType)

    def parseGeneralExpression(self, token_type: TokenTypes) -> ExpressionNode:
        cur = self.match(token_type)
        return ExpressionNode(cur)
