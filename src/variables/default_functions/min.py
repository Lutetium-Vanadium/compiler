from variables.FunctionVariable import FunctionVariable
from variables.Variable import Variable
from variables.Scope import Scope
from variables.default_functions.default_tokens import LTToken, textSpan
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundIfStatement import BoundIfStatement
from binder.BoundReturnStatement import BoundReturnStatement
from binder.BoundVariableExpression import BoundVariableExpression

from type_handling.Types import Types

name = "min"
data_type = Types.Int
params = [Variable("a", Types.Int), Variable("b", Types.Int)]

functionScope = Scope({"a": params[0], "b": params[1]})

paramA = BoundVariableExpression("a", data_type, textSpan)
paramB = BoundVariableExpression("b", data_type, textSpan)
# If statement
condition = BoundBinaryExpression(Types.Bool, paramA, LTToken, paramB, textSpan)

returnA = BoundReturnStatement(paramA, textSpan)
thenScope = Scope(parentScope=functionScope)
thenBlock = BoundBlockStatement([returnA], thenScope, data_type, textSpan)

returnB = BoundReturnStatement(paramB, textSpan)
elseScope = Scope(parentScope=functionScope)
elseBlock = BoundBlockStatement([returnB], elseScope, data_type, textSpan)

ifStatement = BoundIfStatement(condition, thenBlock, elseBlock, textSpan)

functionBody = BoundBlockStatement(
    [ifStatement], functionScope, data_type, textSpan, True
)
min_func = FunctionVariable(name, data_type, params)
min_func.addBody(functionBody)
