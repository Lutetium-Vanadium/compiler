from lexer import Lexer
from token_handling.TokenTypes import *
from token_handling.Token import *
from syntax_tree.BinaryNode import *
from syntax_tree.UnaryNode import *


class Parser:
    def __init__(self, errorBag):
        self.tokenList = []
        self.errorBag = errorBag

    def sanitize(self, tokenList):
        for i in range(len(tokenList) - 1, -1, -1):
            if tokenList[i].isInstance(TokenTypes.Bad, TokenTypes.Whitespace):
                tokenList.pop(i)
        return tokenList

    def parse(self, text, variables, debug):
        self.text = text
        self.variables = variables
        lexer = Lexer(self.errorBag)
        # TODO remove EOL_TOKEN at end, should be put manually when language is complete
        self.tokenList = self.sanitize(lexer.lex(text)) + [EOL_TOKEN]

        return self.variables, self.evaluate(self.tokenList, debug)[0]

    def evaluate(self, tokenList, debug):
        i = 0
        start = 0
        if debug:
            print(tokenList)
        val = None

        while i < len(tokenList) - 1:
            if debug:
                print(i)

            if tokenList[i].isInstance(TokenTypes.Variable):
                text = tokenList[i].token.value
                if tokenList[i + 1].isInstance(TokenTypes.AssignmentOperator):
                    prevI = i
                    self.variables[text], i = self.evaluate(tokenList[i + 2 :], debug)
                    i += prevI + 2
                    continue

                val = self.variables.get(text)

                if val == None:
                    self.errorBag.nameError(text)

            elif tokenList[i].isInstance(
                TokenTypes.Number,
                TokenTypes.Boolean,
                *OPERATOR_TYPES,
                TokenTypes.OpenParan
            ):
                while i < len(tokenList) and tokenList[i].isInstance(
                    TokenTypes.Number,
                    TokenTypes.Boolean,
                    *OPERATOR_TYPES,
                    TokenTypes.CloseParan
                ):
                    i += 1
                a = self.evaluateExpression(tokenList[start : i + 1], debug)
                val = a

            i += 1

        return val, i

    def evaluateExpression(self, tokenList, debug=False):
        tokenList = [OPEN_PARAN_TOKEN, *tokenList, CLOSE_PARAN_TOKEN]

        if debug:
            print(tokenList, "\n")

        postFix = []
        opStack = []
        i = 0
        while i < len(tokenList):
            cur = tokenList[i]
            if cur.isInstance(TokenTypes.OpenParan):
                opStack.append(cur)

            elif cur.isInstance(TokenTypes.Number, TokenTypes.Boolean):
                postFix.append(cur)

            elif cur.isInstance(TokenTypes.CloseParan):
                while not opStack[-1].isInstance(TokenTypes.OpenParan):
                    postFix.append(opStack.pop())
                opStack.pop()

            elif cur.isInstance(*OPERATOR_TYPES):
                if (
                    cur.isInstance(TokenTypes.NotOperator)
                    or i > 0
                    and tokenList[i - 1].isInstance(*OPERATOR_TYPES)
                ):
                    if i <= len(tokenList) - 1:
                        postFix.append(UnaryOperatorNode(tokenList[i + 1], cur))
                    else:
                        self.errorBag.syntaxError(self.text)
                    i += 2
                    continue

                while (
                    OPERATOR_PRECEDENCE[opStack[-1].token_type]
                    > OPERATOR_PRECEDENCE[cur.token_type]
                ):
                    postFix.append(opStack.pop())
                opStack.append(cur)

            if debug:
                print("\nCUR: ", cur.token_type, cur.token.value)
                print("OPSTACK:", opStack)
                print("POSTFIX:", postFix)
                print("IS OPERATOR:", cur.isInstance(*OPERATOR_TYPES))

            i += 1

        if debug:
            print("\n")
            print("FINAL POSTFIX:", postFix)
            print("FINAL OPSTACK:", opStack)

        ansStack = []
        for cur in postFix:
            if isinstance(cur, UnaryOperatorNode) or cur.isInstance(
                TokenTypes.Number, TokenTypes.Boolean
            ):
                ansStack.append(cur)
            elif cur.isInstance(*OPERATOR_TYPES):
                b = ansStack.pop()
                a = ansStack.pop()

                ansStack.append(BinaryOperatorNode(a, b, cur))

        if debug:
            print("\n")
            print(ansStack)

        return ansStack[0]
