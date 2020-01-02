from type_handling.Types import Types
from variables.default_functions.InbuiltFunctions import InbuiltFunctions

class FunctionVariable:
    def __init__(self, name, data_type, params, functionBody, text_span=None):
        self.name = name
        self.params = params
        self.functionBody = functionBody
        self.type = data_type
        self.text_span = text_span

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def addBody(self, functionBody):
        self.functionBody = functionBody

    def get_txt(self):
        return f"{self.name} => {self.type}"

    def get_children(self):
        return []
