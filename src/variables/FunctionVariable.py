from type_handling.Types import Types


class FunctionVariable:
    def __init__(self, name, data_type, params, functionBody):
        self.name = name
        self.value = name
        self.type = data_type
        self.params = params
        self.functionBody = functionBody

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
