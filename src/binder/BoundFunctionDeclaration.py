from binder.BoundDeclarationExpression import BoundDeclarationExpression


class BoundFunctionDeclaration(BoundDeclarationExpression):
    def __init__(
        self, declarationKeyword, expressionType, varName, varValue, text_span
    ):
        super().__init__(
            declarationKeyword, expressionType, varName, varValue, text_span
        )

