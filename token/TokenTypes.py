from enum import Enum, auto, unique

@unique
class TokenTypes(Enum):
    # Type Constants

    # Regular Text
    Whitespace = auto()
    Text = auto()
    Number = auto()
    Boolean = auto()
    EOL = auto()

    # General type for Operators during lexing
    Operator = auto()

    # Operators
    PlusOperator = auto()           # +
    MinusOperator = auto()          # -
    StarOperator = auto()           # *
    SlashOperator = auto()          # /
    ModOperator = auto()            # %
    CarotOperator = auto()          # ^

    # Boolean Operators
    OrOperator = auto()             # ||
    EEOperator = auto()             # ==
    AndOperator = auto()            # &&
    LTOperator = auto()             # <
    GTOperator = auto()             # >
    LEOperator = auto()             # <=
    GEOperator = auto()             # >=

    AssignmentOperator = auto()     # =
    OpenParan = auto()              # (
    CloseParan = auto()             # )

    # Unknown
    Bad = auto()

OPERATOR_TYPES = (
    TokenTypes.PlusOperator,
    TokenTypes.MinusOperator,
    TokenTypes.StarOperator,
    TokenTypes.SlashOperator,
    TokenTypes.ModOperator,
    TokenTypes.CarotOperator,
    TokenTypes.OpenParan,
    TokenTypes.CloseParan,
    TokenTypes.OrOperator,
    TokenTypes.AndOperator,
    TokenTypes.EEOperator,
    TokenTypes.LTOperator,
    TokenTypes.GTOperator,
    TokenTypes.LEOperator,
    TokenTypes.GEOperator,
    TokenTypes.AssignmentOperator
)

OPERATOR_PRECEDENCE = {
    TokenTypes.OpenParan:      -1,
    TokenTypes.CloseParan:     -1,
    TokenTypes.OrOperator:      0,
    TokenTypes.AndOperator:     1,
    TokenTypes.EEOperator:      2,
    TokenTypes.LTOperator:      2,
    TokenTypes.GTOperator:      2,
    TokenTypes.LEOperator:      2,
    TokenTypes.GEOperator:      2,
    TokenTypes.PlusOperator:    3,
    TokenTypes.MinusOperator:   3,
    TokenTypes.StarOperator:    4,
    TokenTypes.SlashOperator:   4,
    TokenTypes.ModOperator:     5,
    TokenTypes.CarotOperator:   6,
}

ARITHMETIC_OPERATORS = (
    TokenTypes.PlusOperator,
    TokenTypes.MinusOperator,
    TokenTypes.StarOperator,
    TokenTypes.SlashOperator,
    TokenTypes.ModOperator,
    TokenTypes.CarotOperator
)

BOOLEAN_OPERATORS = (
    TokenTypes.OrOperator,
    TokenTypes.EEOperator,
    TokenTypes.AndOperator,
    TokenTypes.LTOperator,
    TokenTypes.GTOperator,
    TokenTypes.LEOperator,
    TokenTypes.GEOperator
)