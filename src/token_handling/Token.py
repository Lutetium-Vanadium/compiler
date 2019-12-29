from textSpan import TextSpan
from token_handling.TokenTypes import TokenTypes
from token_handling.TokenValue import TokenValue


class Token:
    def __init__(self, value, token_type, start, length=None):
        self.token_type = token_type
        self.token_value = TokenValue(value, token_type)
        if length == None:
            self.text_span = TextSpan(start, len(str(value)))
        else:
            self.text_span = TextSpan(start, length)

    def __repr__(self):
        return f"Value: '{self.token_value.value}', Type: {self.token_type}"

    def __str__(self):
        return f"Value: '{self.token_value.value}', Type: {self.token_type}"

    def isInstance(self, *args):
        return self.token_type in args

    def isType(self, *args):
        return self.token_value.type in args

    def evaluate(self):
        return self.token_value.value


EOF_TOKEN = Token(";", TokenTypes.EOF, -1)
