class BoundAssignmentExpression:
    def __init__(self, expressionType, varName, varValue, text_span):
        self.type = expressionType
        self.varName = varName
        self.varValue = varValue
        self.text_span = text_span
