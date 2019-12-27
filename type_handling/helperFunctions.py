from token_handling.TokenTypes import TokenTypes


def getBinaryOperatorTypes(operator):
    # Arithmetic Operators
    if self.operatorToken.isInstance(
        TokenTypes.PlusOperator,
        TokenTypes.MinusOperator,
        TokenTypes.StarOperator,
        TokenTypes.SlashOperator,
        TokenTypes.ModOperator,
        TokenTypes.CaretOperator,
    ):
        return int, int

    # Boolean Operators
    if self.operatorToken.isInstance(TokenTypes.OrOperator, TokenTypes.AndOperator):
        return bool, bool

    if self.operatorToken.isInstance(
        TokenTypes.NEOperator,
        TokenTypes.EEOperator,
        TokenTypes.GEOperator,
        TokenTypes.GTOperator,
        TokenTypes.LEOperator,
        TokenTypes.LTOperator,
    ):
        return int, bool

    raise EnvironmentError("Python is dying")
