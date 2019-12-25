class Variable:
    def __init__(self, name, data_type=None, value=None):
        self.name = name
        self.type = data_type
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def evaluate(self):
        return self.value
