from token_handleing.TokenTypes import *
from token_handleing.Token import Token
from keywords.Keywords import KEYWORDS

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
            # A generalised operator type, will be seperated out to the various operators later
            return TokenTypes.Operator

        if char.isdigit() or char == ".":
            return TokenTypes.Number

        self.errorBag.badCharError(char)
        return TokenTypes.Bad

    def get_current_type(self):
        return self.get_type(self.text[self.index])

    def lex(self, text):
        self.text = text
        self.list = []
        self.index = 0
        self.split()
        # print("\n", self, "\n")
        return self.list

    def appendToken(self, word, word_type):
        self.list.append(Token(word, word_type))

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
        return self.text[start : self.index]

    def lexWhitespace(self):
        whitespace = self.get_same_block(TokenTypes.Whitespace)
        self.appendToken(whitespace, TokenTypes.Whitespace)

    def lexText(self):
        text = self.get_same_block(TokenTypes.Text)

        if text in KEYWORDS:
            self.appendToken(text, TokenTypes.Keyword)
        elif text == "true" or text == "false":
            self.appendToken(text == "true", TokenTypes.Boolean)
        else:
            self.appendToken(text, TokenTypes.Variable)

    def lexNumber(self):
        num = self.get_same_block(TokenTypes.Number)
        num = float(num)
        if num.is_integer():
            num = int(num)
        self.appendToken(num, TokenTypes.Number)

    def lexOperator(self):
        cur = self.text[self.index]
        if self.index < len(self.text) - 1:
            nxt = self.text[self.index + 1]
        else:
            nxt = "\0"
        self.index += 1

        if cur == "+":
            self.appendToken("+", TokenTypes.PlusOperator)
        elif cur == "-":
            self.appendToken("-", TokenTypes.MinusOperator)
        elif cur == "*":
            self.appendToken("*", TokenTypes.StarOperator)
        elif cur == "/":
            self.appendToken("/", TokenTypes.SlashOperator)
        elif cur == "%":
            self.appendToken("%", TokenTypes.ModOperator)
        elif cur == "^":
            self.appendToken("^", TokenTypes.CarotOperator)
        elif cur == "(":
            self.appendToken("(", TokenTypes.OpenParan)
        elif cur == ")":
            self.appendToken(")", TokenTypes.CloseParan)
        elif cur == nxt == "|":
            self.index += 1
            self.appendToken("||", TokenTypes.OrOperator)
        elif cur == nxt == "&":
            self.index += 1
            self.appendToken("&&", TokenTypes.AndOperator)
        elif cur == "!":
            if nxt == "=":
                self.index += 1
                self.appendToken("!=", TokenTypes.NEOperator)
            else:
                self.appendToken("!", TokenTypes.NotOperator)
        elif cur == ">":
            if nxt == "=":
                self.index += 1
                self.appendToken(">=", TokenTypes.GEOperator)
            else:
                self.appendToken(">", TokenTypes.GTOperator)
        elif cur == "<":
            if nxt == "=":
                self.index += 1
                self.appendToken("<=", TokenTypes.LEOperator)
            else:
                self.appendToken("<", TokenTypes.LTOperator)
        elif cur == "=":
            if nxt == "=":
                self.index += 1
                self.appendToken("==", TokenTypes.EEOperator)
            else:
                self.appendToken("=", TokenTypes.AssignmentOperator)

        else:
            raise SyntaxError("Unknown Operator ", cur, nxt)
