from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundIfStatement import BoundIfStatement
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundReturnStatement import BoundReturnStatement
from binder.BoundVariableExpression import BoundVariableExpression

from type_handling.Types import Types

from variables.default_functions.default_tokens import GTToken, textSpan
from variables.FunctionVariable import FunctionVariable
from variables.Scope import Scope
from variables.Variable import Variable

name = "max"
data_type = Types.Int
params = [Variable("a", Types.Int), Variable("b", Types.Int)]
funcScope = Scope()

scope = Scope(funcScope)

paramA = BoundVariableExpression("a", data_type, textSpan)
paramB = BoundVariableExpression("b", data_type, textSpan)

# If statement
condition = BoundBinaryExpression(Types.Bool, paramA, GTToken, paramB, textSpan)

returnA = BoundReturnStatement(paramA, textSpan)
thenBlock = BoundBlockStatement([returnA], scope, data_type, textSpan, False)

returnB = BoundReturnStatement(paramB, textSpan)
elseBlock = BoundBlockStatement([returnB], scope, data_type, textSpan, False)

ifStatement = BoundIfStatement(condition, thenBlock, elseBlock, textSpan)

functionBody = BoundBlockStatement([ifStatement], funcScope, data_type, textSpan, True)

max_func = FunctionVariable(name, data_type, params, functionBody)
