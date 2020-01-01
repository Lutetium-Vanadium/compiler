from binder.BoundNode import BoundNode


class BoundFunctionCall(BoundNode):
    def __init__(self, name, paramValues, return_type, text_span):
        self.name = name
        self.paramValues = paramValues
        self.text_span = text_span
        self.type = return_type

    def __repr__(self):
        return f"BoundFunctionCall => {self.type}"

    def __str__(self):
        return f"BoundFunctionCall => {self.type}"

    def get_txt(self):
        return self.__str__()

