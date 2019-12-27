from token_handling.TokenTypes import TokenTypes
from type_handling.Types import Types


def getBinaryOperatorTypes(operator):
    # Arithmetic Operators
    if operator.isInstance(
        TokenTypes.PlusOperator,
        TokenTypes.MinusOperator,
        TokenTypes.StarOperator,
        TokenTypes.SlashOperator,
        TokenTypes.ModOperator,
        TokenTypes.CaretOperator,
    ):
        return Types.Int, Types.Int

    # Boolean Operators
    if operator.isInstance(TokenTypes.OrOperator, TokenTypes.AndOperator):
        return Types.Bool, Types.Bool

    if operator.isInstance(
        TokenTypes.NEOperator,
        TokenTypes.EEOperator,
        TokenTypes.GEOperator,
        TokenTypes.GTOperator,
        TokenTypes.LEOperator,
        TokenTypes.LTOperator,
    ):
        return Types.Int, Types.Bool

    raise EnvironmentError("Python is dying")


def getUnaryOperatorTypes(operator):
    if self.operatorToken.isInstance(
        TokenTypes.MinusOperator,
        TokenTypes.PlusOperator,
        TokenTypes.PlusPlusOperator,
        TokenTypes.MinusMinusOperator,
    ):
        return Types.Int, Types.Int

    if self.operatorToken.isInstance(TokenTypes.NotOperator):
        return Types.Bool, Types.Bool
