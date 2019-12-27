from variables.Variable import Variable
from error.ErrorBag import ErrorBag


class VariableBag:
    def __init__(self):
        self.variables = {}

    def tryInitialiseVariable(self, varName, varValue, varType, isConst):
        var = Variable(varName, varType, varValue, isConst)
        variable = self.variables.get(varName)
        if variable:
            return False

        self.variables[varName] = var
        return True

    def tryGetVariable(self, varName):
        variable = self.variables.get(varName)

        if variable:
            return True, variable
        return False, None

    def updateValue(self, varName, newValue):
        self.variables[varName].trySetValue(newValue)
