from textSpan import TextSpan
from token_handling.TokenTypes import TokenTypes


class Token:
    def __init__(self, value, token_type, start, length=None):
        self.token_type = token_type
        self.value = value

        if length == None:
            self.text_span = TextSpan(start, len(str(value)))
        else:
            self.text_span = TextSpan(start, length)

    def __repr__(self):
        return f"Value: '{self.value}', Type: {self.token_type}"

    def __str__(self):
        return f"Value: '{self.value}', Type: {self.token_type}"

    def isInstance(self, *args):
        return self.token_type in args

EOF_TOKEN = Token("\0", TokenTypes.EOF, -1)
