from syntax_tree.parser import Parser
from syntax_tree.lexer import Lexer
from Evaluator import Evaluator
from binder.Binder import Binder
from error.ErrorBag import ErrorBag
from variables.Scope import Scope
from variables.default_functions import defaultFunctions
from pointers import ptr
import os


def run_multiple_expressions(txt_lst, expected_type="string", returnType="single"):
    """
    txt_lst: List of commands to run
    expected_type: [int, bool, float]
    returnType: Gives return type
            - single: returns last element
            - all: returns the full list 
    """
    errorBag = ErrorBag()
    errorBagPtr = ptr(errorBag)

    scope = Scope()
    scope.addRange(defaultFunctions)
    scopePtr = ptr(scope)

    lexer = Lexer(errorBagPtr)
    parser = Parser(errorBagPtr)
    binder = Binder(errorBagPtr, scopePtr, os.getcwd())
    evaluator = Evaluator(errorBagPtr)

    output_lst = []
    for text in txt_lst:
        errorBag.addText(text)
        tokenList = lexer.lex(text)[1]
        rootNode = parser.parse(tokenList)
        boundTree = binder.bind(rootNode)

        if errorBag.any():
            output_lst.append("ERROR")
        else:
            e = str(evaluator.evaluate(boundTree))
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
