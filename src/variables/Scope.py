from variables.Variable import Variable
from binder.BoundLiteralExpression import BoundLiteralExpression


class Scope:
    def __init__(self, variables={}, parentScope=None):
        self.parentScope = parentScope
        self.variables = variables
        self.isGlobalScope = parentScope == None

    def __repr__(self):
        s = "{\n"
        for k, v in self.variables.items():
            s += f"    '{k}': [ {v} ],\n"
        s += "}"
        return s

    def __str__(self):
        s = "{\n"
        for k, v in self.variables.items():
            s += f"    '{k}': [ {v} ],\n"
        s += "}"
        return s

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

        if self.isGlobalScope:
            return False, None

        return self.parentScope.tryGetVariable(varName)

    def setValue(self, varName, newNode):
        variable = self.variables.get(varName)
        if variable:
            self.variables[varName].trySetValue(newNode)
        elif not self.isGlobalScope:
            self.parentScope.setValue(varName, newNode)

    def updateValue(self, varName, newValue, textSpan):
        success, var = self.tryGetVariable(varName)
        newNode = BoundLiteralExpression(var.type, newValue, textSpan)
        self.setValue(varName, newNode)
