from textSpan import TextSpan
from token_handling.TokenTypes import *
from token_handling.Token import Token
from keywords.Keywords import *

OPERATORS = "+-*/%^()|&<=>!"


class Lexer:
    def __init__(self, errorBag):
        self.text = ""
        self.list = []
        self.errorBag = errorBag
        self.index = 0

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)

    def get_type(self, char):
        if char.isspace():
            return TokenTypes.Whitespace

        if char.isalpha():
            return TokenTypes.Text

        if char in OPERATORS:
            # A generalized operator type, will be seperated out to the various operators later
            return TokenTypes.Operator

        if char.isdigit() or char == ".":
            return TokenTypes.Number

        self.errorBag.badCharError(char, TextSpan(self.index, 1))
        return TokenTypes.Bad

    def get_current_type(self):
        return self.get_type(self.text[self.index])

    def lex(self, text):
        self.text = text
        self.list = []
        self.index = 0
        self.split()
        return self.list, self.errorBag

    def appendToken(self, word, word_type, start):
        self.list.append(Token(word, word_type, start))

    def split(self):
        while self.index < len(self.text):
            cur_type = self.get_current_type()

            if cur_type == TokenTypes.Whitespace:
                self.lexWhitespace()

            elif cur_type == TokenTypes.Text:
                self.lexText()

            elif cur_type == TokenTypes.Number:
                self.lexNumber()

            elif cur_type == TokenTypes.Operator:
                self.lexOperator()

            else:
                self.index += 1

    def get_same_block(self, token_type):
        start = self.index
        while self.index < len(self.text) and self.get_current_type() == token_type:
            self.index += 1
        return self.text[start : self.index], start

    def lexWhitespace(self):
        whitespace, start = self.get_same_block(TokenTypes.Whitespace)
        self.appendToken(whitespace, TokenTypes.Whitespace, start)

    def lexText(self):
        text, start = self.get_same_block(TokenTypes.Text)

        if text in KEYWORDS:
            self.appendKeyword(text, start)
        elif text == "true" or text == "false":
            self.appendToken(text == "true", TokenTypes.Boolean, start)
        else:
            self.appendToken(text, TokenTypes.Variable, start)

    def lexNumber(self):
        num, start = self.get_same_block(TokenTypes.Number)
        if num.find(".") == -1:
            num = int(num)
        else:
            num = float(num)
        self.appendToken(num, TokenTypes.Number, start)

    def lexOperator(self):
        start = self.index
        cur = self.text[self.index]
        if self.index < len(self.text) - 1:
            nxt = self.text[self.index + 1]
        else:
            nxt = "\0"
        self.index += 1

        if cur == "+":
            if nxt == "+":
                self.index += 1
                self.appendToken("++", TokenTypes.PlusPlusOperator, start)
            else:
                self.appendToken("+", TokenTypes.PlusOperator, start)
        elif cur == "-":
            if nxt == "-":
                self.index += 1
                self.appendToken("--", TokenTypes.MinusMinusOperator, start)
            else:
                self.appendToken("-", TokenTypes.MinusOperator, start)
        elif cur == "*":
            self.appendToken("*", TokenTypes.StarOperator, start)
        elif cur == "/":
            self.appendToken("/", TokenTypes.SlashOperator, start)
        elif cur == "%":
            self.appendToken("%", TokenTypes.ModOperator, start)
        elif cur == "^":
            self.appendToken("^", TokenTypes.CaretOperator, start)
        elif cur == "(":
            self.appendToken("(", TokenTypes.OpenParan, start)
        elif cur == ")":
            self.appendToken(")", TokenTypes.CloseParan, start)
        elif cur == nxt == "|":
            self.index += 1
            self.appendToken("||", TokenTypes.OrOperator, start)
        elif cur == nxt == "&":
            self.index += 1
            self.appendToken("&&", TokenTypes.AndOperator, start)
        elif cur == "!":
            if nxt == "=":
                self.index += 1
                self.appendToken("!=", TokenTypes.NEOperator, start)
            else:
                self.appendToken("!", TokenTypes.NotOperator, start)
        elif cur == ">":
            if nxt == "=":
                self.index += 1
                self.appendToken(">=", TokenTypes.GEOperator, start)
            else:
                self.appendToken(">", TokenTypes.GTOperator, start)
        elif cur == "<":
            if nxt == "=":
                self.index += 1
                self.appendToken("<=", TokenTypes.LEOperator, start)
            else:
                self.appendToken("<", TokenTypes.LTOperator, start)
        elif cur == "=":
            if nxt == "=":
                self.index += 1
                self.appendToken("==", TokenTypes.EEOperator, start)
            else:
                self.appendToken("=", TokenTypes.AssignmentOperator, start)

        else:
            raise SyntaxError("Unknown Operator ", cur, nxt, sep="")

    def appendKeyword(self, text, start):
        if text in DECLARATION_KEYWORDS:
            self.appendToken(text, TokenTypes.DeclarationKeyword, start)
        else:
            self.appendToken(text, TokenTypes.Keyword, start)
