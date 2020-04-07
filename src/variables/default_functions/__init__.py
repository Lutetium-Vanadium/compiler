from variables.FunctionVariable import FunctionVariable
from variables.Variable import Variable
from variables.default_functions.max import max_func
from variables.default_functions.min import min_func
from type_handling.Types import Types

inbuiltFunctions = {
    "print": FunctionVariable("print", Types.Void, [Variable("text", Types.Any)], None),
    "input": FunctionVariable("input", Types.String, [Variable("prompt", Types.Any)], None),
    "random": FunctionVariable("random", Types.Float, [], None),
}


defaultFunctions = {
    "min": min_func,
    "max": max_func,
}

defaultFunctions.update(inbuiltFunctions)
