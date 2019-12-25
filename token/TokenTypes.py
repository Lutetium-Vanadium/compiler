from enum import Enum, auto, unique

@unique
class TokenTypes(Enum):
    # Type Constants

    # Regular Text
    Whitespace = auto()
    Number = auto()
    Boolean = auto()
    String = auto()
    Variable = auto()
    Keyword = auto()
    EOL = auto()

    # General type for Operators during lexing
    Operator = auto()
    Text = auto()

    # Operators
    PlusOperator = auto()           # +
    MinusOperator = auto()          # -
    StarOperator = auto()           # *
    SlashOperator = auto()          # /
    ModOperator = auto()            # %
    CarotOperator = auto()          # ^
    PlusPlusOperator = auto()       # ++

    # Boolean Operators
    OrOperator = auto()             # ||
    AndOperator = auto()            # &&
    NotOperator = auto()            # !
    NEOperator = auto()             # !=
    EEOperator = auto()             # ==
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
    TokenTypes.PlusPlusOperator,
    TokenTypes.OpenParan,
    TokenTypes.CloseParan,

    TokenTypes.OrOperator,
    TokenTypes.AndOperator,
    TokenTypes.NotOperator,
    TokenTypes.NEOperator,
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
    TokenTypes.NEOperator:      2,
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
    TokenTypes.CarotOperator:   6
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
    TokenTypes.AndOperator,
    TokenTypes.NotOperator,
    TokenTypes.NEOperator,
    TokenTypes.EEOperator,
    TokenTypes.LTOperator,
    TokenTypes.GTOperator,
    TokenTypes.LEOperator,
    TokenTypes.GEOperator
)