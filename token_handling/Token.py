from token_handling.TokenTypes import TokenTypes
from token_handling.TokenValue import TokenValue


class Token:
    def __init__(self, value, token_type):
        self.token = TokenValue(value, token_type)
        self.token_type = token_type

    def __repr__(self):
        return f"Value: '{self.token.value}', Type: {self.token_type}"

    def __str__(self):
        return f"Value: '{self.token.value}', Type: {self.token_type}"

    def isInstance(self, *args):
        return self.token_type in args

    def evaluate(self):
        return self.token.value


OPEN_PARAN_TOKEN = Token("(", TokenTypes.OpenParan)
CLOSE_PARAN_TOKEN = Token(")", TokenTypes.CloseParan)
EOL_TOKEN = Token("\0", TokenTypes.EOL)

