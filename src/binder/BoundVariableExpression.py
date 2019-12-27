class BoundVariableExpression:
    def __init__(self, var, text_span):
        self.type = var.type
        self.var = var
        self.text_span = text_span

    def __repr__(self):
        return str(self.var.value)

    def __str__(self):
        return str(self.var.value)
