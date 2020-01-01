from syntax_tree.parser import Parser
from Evaluator import Evaluator
from binder.Binder import Binder
from error.ErrorBag import ErrorBag
from variables.Scope import Scope
from variables.default_functions import defaultFunctions


def run_multiple_expressions(txt_lst, expected_type="string", returnType="single"):
    """
    txt_lst: List of commands to run
    expected_type: [int, bool, float]
    returnType: Gives return type
            - single: returns last element
            - all: returns the full list 
    """
    scope = Scope()
    scope.addRange(defaultFunctions)
    errorBag = ErrorBag()
    parser = Parser(errorBag)
    output_lst = []
    for text in txt_lst:
        errorBag.addText(text)
        _, rootNode, errorBag = parser.parse(text, errorBag)
        binder = Binder(rootNode, errorBag, scope)
        boundTree, scope, errorBag = binder.bind()

        if errorBag.any():
            output_lst.append("ERROR")
        else:
            evaluator = Evaluator(boundTree)
            e = str(evaluator.evaluate())
            if expected_type == "int":
                e = int(e)
            elif expected_type == "float":
                e = float(e)
            elif expected_type == "bool":
                e = e == "True"

            output_lst.append(e)
    if returnType == "single":
        return output_lst[-1]
    elif returnType == "all":
        return output_lst


def run_expression(text, expected_type="string"):
    return run_multiple_expressions([text], expected_type)
