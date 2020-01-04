from textSpan import TextSpan
from token_handling.TokenTypes import *
from token_handling.Token import Token
from keywords.Keywords import *
from pointers import ptrVal, pointer
from error.ErrorBag import ErrorBag

SPECIAL_CHARACTERS = "{([+-*/%^|!&<=>,])}"

STRING_MARKERS = "\"'`"


class Lexer:
    def __init__(self, errorBagPtr):
        self.text = ""
        self.list = []
        self._errorBagPtr = errorBagPtr
        self.index = 0
        self.openBrace = 0
        self.closeBrace = 0

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)

    @property
    def cur(self) -> chr:
        return self.text[self.index]

    @property
    def next(self) -> chr:
        if self.index + 1 == len(self.text):
            return "\0"
        return self.text[self.index + 1]

    @property
    def cur_type(self) -> TokenTypes:
        return self.get_type(self.cur)

    @property
    def errorBag(self) -> ErrorBag:
        return ptrVal(self._errorBagPtr)

    def get_type(self, char: str) -> TokenTypes:
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

    def lex(self, text: str) -> (bool, list):
        self.text = text
        self.list = []
        self.index = 0
        self.openBrace = 0
        self.closeBrace = 0
        self.split()

        if self.openBrace > self.closeBrace:
            return True, self.list
        elif self.openBrace < self.closeBrace:
            return False, self.list
        return False, self.list

    def appendToken(self, word: str, word_type: TokenTypes, start: int, length=None):
        self.list.append(Token(word, word_type, start, length))

    def split(self):
        while self.index < len(self.text):
            if self.cur_type == TokenTypes.Whitespace:
                self.lexWhitespace()

            elif self.cur_type == TokenTypes.Text:
                self.lexText()

            elif self.cur_type == TokenTypes.Number and self.cur != ".":
                self.lexNumber()

            elif self.cur_type == TokenTypes.Number and self.next.isdigit():
                self.lexNumber()

            elif self.cur_type == TokenTypes.StringMarker:
                self.lexString()

            elif self.cur_type == TokenTypes.Special:
                self.lexOperator()

            else:
                self.index += 1

    def get_same_block(self, token_type: TokenTypes) -> (str, int):
        start = self.index
        while self.index < len(self.text) and self.cur_type == token_type:
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
        cur = self.cur
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
            if self.cur == "\\":
                self.index += 1
            elif self.cur == "{":
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
            elif self.cur == cur:
                break
            string += self.cur
            self.index += 1
        self.index += 1
        self.appendToken(string, TokenTypes.String, start - 1, self.index - start + 1)

    def lexTemplatedLiteral(self):
        count = 0
        while self.index < len(self.text):
            if self.cur == "{":
                count += 1
            if count == 0 and self.cur == "}":
                return

            if self.cur_type == TokenTypes.Whitespace:
                self.lexWhitespace()

            elif self.cur_type == TokenTypes.Text:
                self.lexText()

            elif self.cur_type == TokenTypes.Number and self.cur != ".":
                self.lexNumber()

            elif self.cur_type == TokenTypes.Number and self.next.isdigit():
                self.lexNumber()

            elif self.cur_type == TokenTypes.StringMarker:
                self.lexString()

            elif self.cur_type == TokenTypes.Special:
                self.lexOperator()

            else:
                self.index += 1

    def lexOperator(self):
        start = self.index

        if self.cur == ",":
            self.index += 1
            self.appendToken(",", TokenTypes.CommaToken, start)
            return
        if self.cur == "+":
            self.index += 1
            if self.cur == "+":
                self.index += 1
                self.appendToken("++", TokenTypes.PlusPlusOperator, start)
                return
            self.appendToken("+", TokenTypes.PlusOperator, start)
            return
        if self.cur == "-":
            self.index += 1
            if self.cur == "-":
                self.index += 1
                self.appendToken("--", TokenTypes.MinusMinusOperator, start)
                return
            self.appendToken("-", TokenTypes.MinusOperator, start)
            return
        if self.cur == "*":
            self.index += 1
            self.appendToken("*", TokenTypes.StarOperator, start)
            return
        if self.cur == "/":
            self.index += 1
            self.appendToken("/", TokenTypes.SlashOperator, start)
            return
        if self.cur == "%":
            self.index += 1
            self.appendToken("%", TokenTypes.ModOperator, start)
            return
        if self.cur == "^":
            self.index += 1
            self.appendToken("^", TokenTypes.CaretOperator, start)
            return
        if self.cur == "(":
            self.index += 1
            self.appendToken("(", TokenTypes.OpenParan, start)
            return
        if self.cur == ")":
            self.index += 1
            self.appendToken(")", TokenTypes.CloseParan, start)
            return
        if self.cur == "{":
            self.index += 1
            self.openBrace += 1
            self.appendToken("{", TokenTypes.OpenBrace, start)
            return
        if self.cur == "}":
            self.index += 1
            self.closeBrace += 1
            self.appendToken("}", TokenTypes.CloseBrace, start)
            return
        if self.cur == "[":
            self.index += 1
            self.appendToken("[", TokenTypes.OpenBracket, start)
            return
        if self.cur == "]":
            self.index += 1
            self.appendToken("]", TokenTypes.CloseBracket, start)
            return
        if self.cur == self.next == "|":
            self.index += 2
            self.appendToken("||", TokenTypes.OrOperator, start)
            return
        if self.cur == self.next == "&":
            self.index += 2
            self.appendToken("&&", TokenTypes.AndOperator, start)
            return
        if self.cur == "!":
            self.index += 1
            if self.cur == "=":
                self.index += 1
                self.appendToken("!=", TokenTypes.NEOperator, start)
                return
            self.appendToken("!", TokenTypes.NotOperator, start)
            return
        if self.cur == ">":
            self.index += 1
            if self.cur == "=":
                self.index += 1
                self.appendToken(">=", TokenTypes.GEOperator, start)
                return
            self.appendToken(">", TokenTypes.GTOperator, start)
            return
        if self.cur == "<":
            self.index += 1
            if self.cur == "=":
                self.index += 1
                self.appendToken("<=", TokenTypes.LEOperator, start)
                return
            self.appendToken("<", TokenTypes.LTOperator, start)
            return
        if self.cur == "=":
            self.index += 1
            if self.cur == "=":
                self.index += 1
                self.appendToken("==", TokenTypes.EEOperator, start)
                return
            self.appendToken("=", TokenTypes.AssignmentOperator, start)
            return

        raise SyntaxError(f"Unknown Operator {self.cur}{self.next}")

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
