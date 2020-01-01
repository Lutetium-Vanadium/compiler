#!/usr/bin/python3
import os, sys
from error.ErrorBag import ErrorBag
from Evaluator import Evaluator
from syntax_tree.parser import Parser
from binder.Binder import Binder
from variables.default_functions import defaultFunctions

from variables.Scope import Scope
from variables.functions import functions
import readline

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

parser = Parser(errorBag)

bash = False
globalScope = Scope()
globalScope.addRange(defaultFunctions)
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
    continueToNextLine, rootNode, errorBag = parser.parse(expression, errorBag)
    if continueToNextLine:
        continue
    else:
        expression = ""
        indent = ""
    binder = Binder(rootNode, errorBag, globalScope)
    boundTree, globalScope, errorBag = binder.bind()

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
            
        evaluator = Evaluator(boundTree)
        print(evaluator.evaluate())
