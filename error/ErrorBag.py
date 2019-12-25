from error.Error import Error
from printing.print_color import print_color, RED


class ErrorBag:
    def __init__(self, previousErrorBag=None):
        self.errors = []
        if previousErrorBag:
            self.errors = previousErrorBag.getErrors()

    def any(self):
        return any(self.errors)

    def getErrors(self):
        return self.errors

    def prt(self):
        print()
        for error in self.errors:
            print_color("   ", error, fg=RED)
        print()

    def clear(self):
        self.errors.clear()

    def report(self, err):
        self.errors.append(err)

    def badCharError(self, char):
        self.report(Error(f"BadCharacterError: Unrecognised character {char}"))

    def typeError(self, typeGotten, expectedType):
        self.report(
            Error(f"TypeError: Expected type {expectedType}, got type {typeGotten}")
        )

    def syntaxError(self, text, reason=""):
        if len(reason) > 0:
            reason = "\n  - " + reason
        self.report(Error(f"SyntaxError: {text} is syntactically incorrect.{reason}"))

    def nameError(self, name):
        self.report(Error(f"NameError: {name} is not a variable"))
