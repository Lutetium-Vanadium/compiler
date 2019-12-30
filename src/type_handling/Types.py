from enum import Enum, auto, unique


@unique
class Types(Enum):
    Any = auto()
    Bool = auto()
    Float = auto()
    Int = auto()
    String = auto()
    Unknown = auto()
    Void = auto()
