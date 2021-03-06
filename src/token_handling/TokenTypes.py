from enum import Enum, auto, unique


@unique
class TokenTypes(Enum):
    # Regular Text
    Whitespace = auto()
    Number = auto()
    Boolean = auto()
    String = auto()
    Variable = auto()
    List = auto()
    Function = auto()
    EOL = auto()
    EOF = auto()

    # Seperators
    CommaToken = auto()

    # Keywords
    Keyword = auto()
    DeclarationKeyword = auto()
    IfKeyword = auto()
    ElseKeyword = auto()
    WhileKeyword = auto()
    ForKeyword = auto()
    InKeyword = auto()
    RangeKeyword = auto()
    ReturnKeyword = auto()

    # General types during lexing
    Special = auto()
    Text = auto()
    StringMarker = auto()

    # Operators
    PlusOperator = auto()  #            +
    MinusOperator = auto()  #           -
    StarOperator = auto()  #            *
    SlashOperator = auto()  #           /
    ModOperator = auto()  #             %
    CaretOperator = auto()  #           ^
    PlusPlusOperator = auto()  #        ++
    MinusMinusOperator = auto()  #      --
    AssignmentOperator = auto()  #      =

    # Boolean Operators
    OrOperator = auto()  #              ||
    AndOperator = auto()  #             &&
    NotOperator = auto()  #             !
    NEOperator = auto()  #              !=
    EEOperator = auto()  #              ==
    LTOperator = auto()  #              <
    GTOperator = auto()  #              >
    LEOperator = auto()  #              <=
    GEOperator = auto()  #              >=

    # String markers
    SingleQuote = auto()  #             '
    DoubleQuote = auto()  #             "
    BackTick = auto()  #                `

    # Brackets
    OpenParan = auto()  #               (
    CloseParan = auto()  #              )
    OpenBrace = auto()  #               {
    CloseBrace = auto()  #              }
    OpenBracket = auto()  #             [
    CloseBracket = auto()  #            ]

    # Unknown
    Bad = auto()


CALC_ASSIGN_OPERATORS = (
    TokenTypes.PlusOperator,
    TokenTypes.MinusOperator,
    TokenTypes.StarOperator,
    TokenTypes.SlashOperator,
    TokenTypes.ModOperator,
    TokenTypes.OrOperator,
    TokenTypes.AndOperator,
)

STRING_MARKERS = (TokenTypes.BackTick, TokenTypes.DoubleQuote, TokenTypes.SingleQuote)


def getUnaryPrecedence(token):
    if token.isInstance(
        TokenTypes.NotOperator,
        TokenTypes.PlusOperator,
        TokenTypes.MinusOperator,
        TokenTypes.MinusMinusOperator,
        TokenTypes.PlusPlusOperator,
    ):
        return 8
    return 0


def getBinaryPrecedence(token):
    if token.isInstance(TokenTypes.CaretOperator):
        return 7
    if token.isInstance(TokenTypes.ModOperator):
        return 6
    if token.isInstance(TokenTypes.SlashOperator, TokenTypes.StarOperator):
        return 5
    if token.isInstance(TokenTypes.PlusOperator, TokenTypes.MinusOperator):
        return 4
    if token.isInstance(
        TokenTypes.NEOperator,
        TokenTypes.EEOperator,
        TokenTypes.LTOperator,
        TokenTypes.GTOperator,
        TokenTypes.LEOperator,
        TokenTypes.GEOperator,
    ):
        return 3
    if token.isInstance(TokenTypes.AndOperator):
        return 2
    if token.isInstance(TokenTypes.OrOperator):
        return 1
    return 0
