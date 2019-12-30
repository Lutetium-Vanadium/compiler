from type_handling.Types import Types


class Variable:
    def __init__(self, name, data_type=None, value=None, isConst=False):
        self.name = name
        self.type = data_type
        self.value = value
        self.isConst = isConst

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def setType(self, value):
        if type(value) == int:
            self.type = Types.Int
        elif type(value) == float:
            self.type = Types.Float
        elif type(value) == str:
            self.type = Types.String
        elif type(value) == bool:
            self.type = Types.Bool

    def trySetValue(self, value):
        if self.type == None:
            self.setType(value)
        if self.isConst and self.value != None:
            return False

        self.value = value
        return True


def getStatsFromDeclarationKeyword(declarationKeyword):
    if declarationKeyword == "const":
        return None, True
    if declarationKeyword == "var":
        return None, False
    if declarationKeyword == "int":
        return Types.Int, False
    if declarationKeyword == "float":
        return Types.Float, False
    if declarationKeyword == "string":
        return Types.String, False
    if declarationKeyword == "bool":
        return Types.Bool, False
