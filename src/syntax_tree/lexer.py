from textSpan import TextSpan
from token_handling.TokenTypes import *
from token_handling.Token import Token
from keywords.Keywords import *

SPECIAL_CHARACTERS = "+-*/%^(){|&<=>!},"

STRING_MARKERS = "\"'`"


class Lexer:
    def __init__(self, errorBag):
        self.text = ""
        self.list = []
        self.errorBag = errorBag
        self.index = 0
        self.openBrace = 0
        self.closeBrace = 0

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)

    def get_type(self, char: str):
        if char.isspace():
            return TokenTypes.Whitespace

        if char.isalpha():
            return TokenTypes.Text

        if char in SPECIAL_CHARACTERS:
            # A generalized operator type, will be seperated out to the various operators later
            return TokenTypes.Special

        if char in STRING_MARKERS:
            return TokenTypes.StringMarker

        if char.isdigit() or char == ".":
            return TokenTypes.Number

        self.errorBag.badCharError(char, TextSpan(self.index, 1))
        return TokenTypes.Bad

    def get_current_type(self):
        return self.get_type(self.text[self.index])

    def lex(self, text: str):
        self.text = text
        self.list = []
        self.index = 0
        self.split()
        if self.openBrace > self.closeBrace:
            return True, self.list, self.errorBag
        elif self.openBrace < self.closeBrace:
            return False, self.list, self.errorBag
        return False, self.list, self.errorBag

    def appendToken(self, word: str, word_type: TokenTypes, start: int, length=None):
        self.list.append(Token(word, word_type, start, length))

    def split(self):
        while self.index < len(self.text):
            cur_type = self.get_current_type()

            if cur_type == TokenTypes.Whitespace:
                self.lexWhitespace()

            elif cur_type == TokenTypes.Text:
                self.lexText()

            elif cur_type == TokenTypes.Number and self.text[self.index] != ".":
                self.lexNumber()

            elif cur_type == TokenTypes.Number and self.text[self.index + 1].isdigit():
                self.lexNumber()

            elif cur_type == TokenTypes.StringMarker:
                self.lexString()

            elif cur_type == TokenTypes.Special:
                self.lexOperator()

            else:
                self.index += 1

    def get_same_block(self, token_type: TokenTypes):
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

    def lexString(self):
        cur = self.text[self.index]
        if cur == '"':
            token = TokenTypes.DoubleQuote
        elif cur == "'":
            token = TokenTypes.SingleQuote
        elif cur == "`":
            token = TokenTypes.BackTick
        else:
            raise Exception(f"Unknown starter, '{cur}'")

        self.index += 1

        templated = cur == "`"

        string = ""
        start = self.index
        while self.index < len(self.text):
            if self.text[self.index] == "\\":
                self.index += 1
            elif self.text[self.index] == "{":
                self.appendToken(string, TokenTypes.String, start - 1)
                self.appendToken("+", TokenTypes.PlusOperator, self.index)
                self.appendToken("(", TokenTypes.OpenParan, self.index)
                self.index += 1
                self.lexTemplatedLiteral()
                self.appendToken(")", TokenTypes.CloseParan, self.index)
                self.appendToken("+", TokenTypes.PlusOperator, self.index)
                self.index += 1
                string = ""
                continue
            elif self.text[self.index] == cur:
                break
            string += self.text[self.index]
            self.index += 1
        self.index += 1
        self.appendToken(string, TokenTypes.String, start - 1, self.index - start + 1)

    def lexTemplatedLiteral(self):
        count = 0
        while self.index < len(self.text):
            if self.text[self.index] == "{":
                count += 1
            if count == 0 and self.text[self.index] == "}":
                return

            cur_type = self.get_current_type()

            if cur_type == TokenTypes.Whitespace:
                self.lexWhitespace()

            elif cur_type == TokenTypes.Text:
                self.lexText()

            elif cur_type == TokenTypes.Number and self.text[self.index] != ".":
                self.lexNumber()

            elif cur_type == TokenTypes.Number and self.text[self.index + 1].isdigit():
                self.lexNumber()

            elif cur_type == TokenTypes.StringMarker:
                self.lexString()

            elif cur_type == TokenTypes.Special:
                self.lexOperator()

            else:
                self.index += 1

    def lexOperator(self):
        start = self.index
        cur = self.text[self.index]
        if self.index < len(self.text) - 1:
            nxt = self.text[self.index + 1]
        else:
            nxt = "\0"
        self.index += 1

        if cur == ",":
            self.appendToken(",", TokenTypes.CommaToken, start)
            return
        if cur == "+":
            if nxt == "+":
                self.index += 1
                self.appendToken("++", TokenTypes.PlusPlusOperator, start)
                return
            self.appendToken("+", TokenTypes.PlusOperator, start)
            return
        if cur == "-":
            if nxt == "-":
                self.index += 1
                self.appendToken("--", TokenTypes.MinusMinusOperator, start)
                return
            self.appendToken("-", TokenTypes.MinusOperator, start)
            return
        if cur == "*":
            self.appendToken("*", TokenTypes.StarOperator, start)
            return
        if cur == "/":
            self.appendToken("/", TokenTypes.SlashOperator, start)
            return
        if cur == "%":
            self.appendToken("%", TokenTypes.ModOperator, start)
            return
        if cur == "^":
            self.appendToken("^", TokenTypes.CaretOperator, start)
            return
        if cur == "(":
            self.appendToken("(", TokenTypes.OpenParan, start)
            return
        if cur == ")":
            self.appendToken(")", TokenTypes.CloseParan, start)
            return
        if cur == "{":
            self.openBrace += 1
            self.appendToken("{", TokenTypes.OpenBrace, start)
            return
        if cur == "}":
            self.closeBrace += 1
            self.appendToken("}", TokenTypes.CloseBrace, start)
            return
        if cur == nxt == "|":
            self.index += 1
            self.appendToken("||", TokenTypes.OrOperator, start)
            return
        if cur == nxt == "&":
            self.index += 1
            self.appendToken("&&", TokenTypes.AndOperator, start)
            return
        if cur == "!":
            if nxt == "=":
                self.index += 1
                self.appendToken("!=", TokenTypes.NEOperator, start)
                return
            self.appendToken("!", TokenTypes.NotOperator, start)
            return
        if cur == ">":
            if nxt == "=":
                self.index += 1
                self.appendToken(">=", TokenTypes.GEOperator, start)
                return
            self.appendToken(">", TokenTypes.GTOperator, start)
            return
        if cur == "<":
            if nxt == "=":
                self.index += 1
                self.appendToken("<=", TokenTypes.LEOperator, start)
                return
            self.appendToken("<", TokenTypes.LTOperator, start)
            return
        if cur == "=":
            if nxt == "=":
                self.index += 1
                self.appendToken("==", TokenTypes.EEOperator, start)
                return
            self.appendToken("=", TokenTypes.AssignmentOperator, start)
            return

        raise SyntaxError(f"Unknown Operator {cur}{nxt}")

    def appendKeyword(self, text: str, start: int):
        if text in DECLARATION_KEYWORDS:
            self.appendToken(text, TokenTypes.DeclarationKeyword, start)
        else:
            self.appendToken(text, self.getTokenFromKeyword(text), start)

    def getTokenFromKeyword(self, keyword: str):
        if keyword == "if":
            return TokenTypes.IfKeyword
        elif keyword == "else":
            return TokenTypes.ElseKeyword
        elif keyword == "while":
            return TokenTypes.WhileKeyword
        elif keyword == "for":
            return TokenTypes.ForKeyword
        elif keyword == "in":
            return TokenTypes.InKeyword
        elif keyword == "range":
            return TokenTypes.RangeKeyword
        elif keyword == "return":
            return TokenTypes.ReturnKeyword

        raise Exception(f"Unknown keyword {keyword}")
