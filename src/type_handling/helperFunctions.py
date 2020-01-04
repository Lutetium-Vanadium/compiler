from token_handling.TokenTypes import TokenTypes
from token_handling.Token import Token
from type_handling.Types import Types
from binder.BoundNode import BoundNode
from error.ErrorBag import ErrorBag
from pointers import ptrVal, pointer


def getUnaryOperatorTypes(operator: Token):
    if operator.isInstance(
        TokenTypes.MinusOperator,
        TokenTypes.PlusOperator,
        TokenTypes.PlusPlusOperator,
        TokenTypes.MinusMinusOperator,
    ):
        return Types.Int, Types.Int

    if operator.isInstance(TokenTypes.NotOperator):
        return Types.Bool, Types.Bool


def getType(value):
    if type(value) == int:
        return Types.Int
    if type(value) == float:
        return Types.Float
    if type(value) == bool:
        return Types.Bool
    if type(value) == str:
        return Types.String
    if type(value) == list:
        return Types.List
    return Types.Unknown


def isNumber(arg: Types):
    return arg == Types.Int or arg == Types.Float


def checkBinaryType(
    operator: Token, left: BoundNode, right: BoundNode, errorBagPtr: pointer
):
    errorBag = ptrVal(errorBagPtr)
    if operator.isInstance(TokenTypes.EEOperator):
        if right.type != left.type:
            errorBag.typeError(right.type, left.type, right.text_span)
        return Types.Bool

    if left.type == Types.String or right.type == Types.String:
        if operator.isInstance(TokenTypes.PlusOperator):
            return Types.String
        if operator.isInstance(TokenTypes.StarOperator):
            if left.type == Types.String and right.type != Types.Int:
                errorBag.typeError(right.type, Types.String, right.text_span)
            if right.type == Types.String and left.type != Types.Int:
                errorBag.typeError(left.type, Types.String, left.text_span)
            return Types.String

    if left.type == Types.List or right.type == Types.String:
        if operator.isInstance(TokenTypes.PlusOperator):
            if left.type == Types.List and right.type != Types.List:
                errorBag.typeError(right.type, Types.List, right.text_span)
            if right.type == Types.List and left.type != Types.List:
                errorBag.typeError(left.type, Types.List, left.text_span)
            return Types.List

        if operator.isInstance(TokenTypes.StarOperator):
            if left.type == Types.List and right.type != Types.Int:
                errorBag.typeError(right.type, Types.List, right.text_span)
            if right.type == Types.List and left.type != Types.Int:
                errorBag.typeError(left.type, Types.List, left.text_span)
            return Types.List

    # Arithmetic Operators
    if operator.isInstance(
        TokenTypes.PlusOperator,
        TokenTypes.MinusOperator,
        TokenTypes.StarOperator,
        TokenTypes.SlashOperator,
        TokenTypes.ModOperator,
        TokenTypes.CaretOperator,
    ):
        if not isNumber(left.type):
            errorBag.typeError(
                left.type, f"{Types.Int}> or <{Types.Float}", left.text_span
            )
        if not isNumber(right.type):
            errorBag.typeError(
                right.type, f"{Types.Int}> or <{Types.Float}", right.text_span
            )
        if left.type == right.type == Types.Int:
            return Types.Int
        return Types.Float

    # Boolean Operators
    if operator.isInstance(TokenTypes.OrOperator, TokenTypes.AndOperator):
        if left.type != Types.Bool:
            errorBag.typeError(left.type, Types.Bool, left.text_span)
        if right.type != Types.Bool:
            errorBag.typeError(right.type, Types.Bool, right.text_span)
        return Types.Bool

    if operator.isInstance(
        TokenTypes.NEOperator,
        TokenTypes.GEOperator,
        TokenTypes.GTOperator,
        TokenTypes.LEOperator,
        TokenTypes.LTOperator,
    ):
        if not isNumber(left.type):
            errorBag.typeError(
                left.type, f"{Types.Int}> or <{Types.Float}", left.text_span
            )
        if not isNumber(right.type):
            errorBag.typeError(
                right.type, f"{Types.Int}> or <{Types.Float}", right.text_span
            )

        return Types.Bool

    raise EnvironmentError("Python is dying")
