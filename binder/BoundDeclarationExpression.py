from binder.BoundAssignmentExpression import BoundAssignmentExpression


class BoundDeclarationExpression(BoundAssignmentExpression):
    def __init__(
        self, declarationKeyword, expressionType, varName, varValue, text_span
    ):
        self.declarationKeyword = declarationKeyword
        super().__init__(expressionType, varName, varValue, text_span)

    def __repr__(self):
        return f"{self.declarationKeyword} {self.varName} = {self.varValue}"

    def __repr__(self):
        return f"{self.declarationKeyword} {self.varName} = {self.varValue}"
