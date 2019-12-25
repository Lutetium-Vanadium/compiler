from TokenTypes import *
from Token import Token

OPERATORS = "+-*/%^()|&<=>"

def getOperatorType(operator):
    if operator == "+":
        return TokenTypes.PlusOperator
    if operator == "-":
        return TokenTypes.MinusOperator
    if operator == "*":
        return TokenTypes.StarOperator
    if operator == "/":
        return TokenTypes.SlashOperator
    if operator == "%":
        return TokenTypes.ModOperator
    if operator == "^":
        return TokenTypes.CarotOperator
    if operator == "(":
        return TokenTypes.OpenParan
    if operator == ")":
        return TokenTypes.CloseParan
    if operator == "||":
        return TokenTypes.OrOperator
    if operator == "&&":
        return TokenTypes.AndOperator
    if operator == ">=":
        return TokenTypes.GEOperator
    if operator == ">":
        return TokenTypes.GTOperator
    if operator == "<=":
        return TokenTypes.LEOperator
    if operator == "<":
        return TokenTypes.LTOperator
    if operator == "==":
        return TokenTypes.EEOperator
    if operator == "=":
        return TokenTypes.AssignmentOperator
    
    # If it reaches here, Python is probably dying, abort
    raise Exception(f"Unrecognised Operator '{operator}'")

class Lexer():
    def __init__(self, errorBag):
        self.text = ""
        self.list = []
        self.errorBag = errorBag
    
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

        try:
            float(char)
            return TokenTypes.Number
        except:
            self.errorBag.badCharError(char)
            return TokenTypes.Bad
    
    def lex(self, text):
        self.text = text
        self.list = []
        self.split()
        # print("\n", self, "\n")
        return self.list
    
    def appendToken(self, word, word_type):
        if word_type == TokenTypes.Number:
            self.list.append(Token(word, word_type))
        elif word_type == TokenTypes.Operator:
            self.list.append(Token(word, getOperatorType(word)))
        elif word_type == TokenTypes.Text and (word == "true" or word == "false"):
            self.list.append(Token(word == "true", TokenTypes.Boolean))
        else:
            self.list.append(Token(word, word_type))

    def split(self):
        word = ""
        word_type = None

        for i in range(len(self.text)):
            cur = self.text[i]
            cur_type = self.get_type(cur)

            if len(word) == 0:
                word_type = cur_type
                word += cur

            elif cur_type == word_type:
                word += cur

            else:
                self.appendToken(word, word_type)
                word = cur
                word_type = cur_type
        
        self.appendToken(word, word_type)