#!/usr/bin/python3
import os, sys
from error.ErrorBag import ErrorBag
from Evaluator import Evaluator
from syntax_tree.lexer import Lexer
from syntax_tree.parser import Parser
from binder.Binder import Binder
from variables.default_functions import defaultFunctions

from variables.Scope import Scope
import readline

from pointers import ptr

showParseTree = "parseTree" in sys.argv
showBoundTree = "boundTree" in sys.argv


def cmd_input(prompt, prefill):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    except:
        return ""
    finally:
        readline.set_startup_hook()


def getIndent(s):
    i = 0
    a = len(s)
    while i < len(s) and s[i] == "\t" or s[i] == " ":
        i += 1
    return s[:i]


errorBag = ErrorBag()
errorBagPtr = ptr(errorBag)

globalScope = Scope()
globalScope.addRange(defaultFunctions)
globalScopePtr = ptr(globalScope)

lexer = Lexer(errorBagPtr)
parser = Parser(errorBagPtr)
binder = Binder(errorBagPtr, globalScopePtr)
evaluator = Evaluator()

bash = False
continueToNextLine = False
expression = ""
indent = ""

while True:
    if bash:
        s = "$ "
    elif showParseTree or showBoundTree:
        if continueToNextLine:
            s = "├·· "
        else:
            s = "┌>> "
    else:
        if continueToNextLine:
            s = "··· "
        else:
            s = ">>> "
    new_expression = cmd_input(s, indent)

    if continueToNextLine:
        indent = getIndent(new_expression)
        new_expression = new_expression.lstrip()

    expression += indent + new_expression

    if len(expression) == 0:
        print()
        continue

    if expression == "exit":
        break
    if bash:
        if expression == "repl":
            bash = False
            expression = ""
            indent = ""
            continue
        os.system(expression)
        expression = ""
        indent = ""
        continue

    if expression == "bash":
        bash = True
        expression = ""
        indent = ""
        continue
    if expression == "parseTree":
        showParseTree = not showParseTree
        if showParseTree:
            print("Showing Parsed Tree.")
        else:
            print("Not showing Parsed Tree.")
        expression = ""
        indent = ""
        continue
    if expression == "boundTree":
        showBoundTree = not showBoundTree
        if showBoundTree:
            print("Showing Bound Tree.")
        else:
            print("Not showing Bound Tree.")
        expression = ""
        indent = ""
        continue
    if expression[0] == "$":
        os.system(expression[1:])
        expression = ""
        indent = ""
        continue
    if expression[0] == "#":
        eval(expression[1:])
        expression = ""
        indent = ""
        continue

    expression += "\n"

    errorBag.addText(expression)
    continueToNextLine, tokenList = lexer.lex(expression)
    if continueToNextLine:
        continue
    else:
        expression = ""
        indent = ""
    rootNode = parser.parse(tokenList)
    boundTree = binder.bind(rootNode)

    if errorBag.any():
        errorBag.prt()
        errorBag.clear()
    else:
        if showParseTree:
            rootNode.prt(rootNode)
            print()
        if showBoundTree:
            boundTree.prt(boundTree)
            print()

        print(evaluator.evaluate(boundTree))
