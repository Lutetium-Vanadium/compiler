from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types


class TokenValue:
    def __init__(self, value, token_type):
        self.value = value
        self.type = self.getType(value)

    def getType(self, value):
        if type(value) == int:
            return Types.Int
        if type(value) == float:
            return Types.Float
        if type(value) == bool:
            return Types.Bool

        return Types.String
