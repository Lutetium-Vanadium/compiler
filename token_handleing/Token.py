from token_handleing.TokenTypes import TokenTypes
from token_handleing.TokenValue import TokenValue


class Token:
    def __init__(self, value, token_type):
        self.token = TokenValue(value, token_type)
        self.token_type = token_type

    def __repr__(self):
        return f"\n\tValue: '{self.token.value}', Type: {self.token_type}\n"

    def __str__(self):
        return f"\n\tValue: '{self.token.value}', Type: {self.token_type}\n"

    def isInstance(self, *args):
        return self.token_type in args

    def evaluate(self):
        return self.token.value


OPEN_PARAN_TOKEN = Token("(", TokenTypes.OpenParan)
CLOSE_PARAN_TOKEN = Token(")", TokenTypes.CloseParan)
EOL_TOKEN = Token(";", TokenTypes.EOL)

