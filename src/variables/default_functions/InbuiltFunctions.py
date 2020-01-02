from enum import Enum, unique, auto


class InbuiltFunctions(Enum):
    Print = auto()
    Input = auto()
    Random = auto()

    # Default for all non python executed functions
    Regular = auto()
