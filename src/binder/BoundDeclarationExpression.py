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

    def get_children(self):
        return super().get_children()

    def get_txt(self):
        return f"BoundDeclaration '{self.declarationKeyword}' for '{self.varName}' - <{self.type}>"
