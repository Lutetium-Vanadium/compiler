from binder.BoundAssignmentExpression import BoundAssignmentExpression


class BoundDeclarationExpression(BoundAssignmentExpression):
    def __init__(
        self, declarationKeyword, expressionType, varName, varValue, text_span
    ):
        self.type = expressionType
        super().__init__(expressionType, varName, varValue, text_span)
