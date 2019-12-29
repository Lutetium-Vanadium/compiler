from error.Error import Error
from printing.print_color import print_color, RED


class ErrorBag:
    def __init__(self, previousErrorBag=None, text=""):
        self.text = text
        self.errors = []
        if previousErrorBag:
            self.errors = previousErrorBag.getErrors()
            self.text = previousErrorBag.text

    def addText(self, text):
        self.text = text

    def any(self):
        return any(self.errors)

    def getErrors(self):
        return self.errors

    def prt(self):
        print()
        for error in self.errors:
            before = self.text[: error.text_span.start]
            cause = self.text[error.text_span.start : error.text_span.end]
            after = self.text[error.text_span.end :]
            print("   ", before, end="")
            print_color(cause, fg=RED, end="")
            print(after)
            print_color(error, "\n", fg=RED)

    def clear(self):
        self.errors.clear()

    def extend(self, errorBag):
        self.errors.extend(errorBag.getErrors())

    def report(self, err):
        self.errors.append(err)

    def badCharError(self, char, text_span):
        self.report(
            Error(f"BadCharacterError: Unrecognized character '{char}'", text_span)
        )

    def tokenError(self, tokenGotten, expectedToken, text_span):
        self.report(
            Error(
                f"TokenError: Expected token <{expectedToken}>, got <{tokenGotten}>",
                text_span,
            )
        )

    def unexpectedToken(self, token, text_span):
        self.report(Error(f"UnexpectedToken: {token}", text_span))

    def typeError(self, typeGotten, expectedType, text_span):
        self.report(
            Error(
                f"TypeError: Expected type <{expectedType}>, got type <{typeGotten}>",
                text_span,
            )
        )

    def assignmentTypeError(self, typeGotten, expectedType, text_span):
        self.report(
            Error(
                f"TypeError: '{typeGotten}' cannot be assigned to variable of type '{typeGotten}'",
                text_span,
            )
        )

    def syntaxError(self, text, text_span, reason=""):
        if len(reason) > 0:
            reason = "\n  - " + reason
        self.report(
            Error(
                f"SyntaxError: `{text}` is syntactically incorrect{reason}", text_span
            )
        )

    def nameError(self, name, text_span):
        self.report(Error(f"NameError: '{name}' is not a variable", text_span))

    def initialiseError(self, name, text_span):
        self.report(Error(f"InitialiseError: '{name}' is already declared", text_span))

    def reassignConstError(self, name, text_span):
        self.report(
            Error(
                f"ReassignConstError: '{name}' is declared as 'const' and cannot be reassigned\
                \n    Use 'int', 'float', 'string', 'bool' or 'var' instead",
                text_span,
            )
        )
