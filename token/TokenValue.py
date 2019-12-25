from TokenTypes import TokenTypes
from Types import Types

class TokenValue():
    def __init__(self, value, token_type):
        if token_type == TokenTypes.Number:
            value = float(value)
            if value.is_integer():
                value = int(value)
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