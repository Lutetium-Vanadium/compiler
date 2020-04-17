from enum import Enum, auto, unique


@unique
class Types(Enum):
    Any = auto()
    Bool = auto()
    Float = auto()
    Int = auto()
    List = auto()
    String = auto()
    Unknown = auto()
    Void = auto()


class List:
    def __init__(self, typ):
        self.type = typ

    def __eq__(self, other):
        if not isinstance(other, List):
            return False
        return self.type == other.type
    
    def __str__(self):
        return f"List<{self.type}>"

    def __repr__(self):
        return f"List<{self.type}>"