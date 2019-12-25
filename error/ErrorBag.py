from Error import Error

class ErrorBag():
    def __init__(self, previousErrorBag = None):
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
            print(f"\033[91m {error} \033[00m")
        print()
    
    def clear(self):
        self.errors.clear()
    
    def report(self, err):
        self.errors.append(err)
    
    def badCharError(self, char):
        self.report(Error(f"BadCharacterError: Unrecognised character {char}"))
    
    def typeError(self, typeGotten, expectedType):
        self.report(Error(f"TypeError: Expected type {expectedType}, got type {typeGotten}"))
    
    def syntaxError(self, text):
        self.report(Error(f"SyntaxError: {text} is syntactically incorrect"))
    
    def nameError(self, name):
        self.report(Error(f"NameError: {name} is not a variable"))