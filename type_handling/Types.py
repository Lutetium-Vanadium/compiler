from enum import Enum, auto, unique


@unique
class Types(Enum):
    Int = auto()
    Float = auto()
    String = auto()
    Bool = auto()
    Unknown = auto()
