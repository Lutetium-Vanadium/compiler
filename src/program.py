#!/usr/bin/python3
import os, sys
from error.ErrorBag import ErrorBag
from Evaluator import Evaluator
from parser import Parser
from binder.Binder import Binder

from variables.Scope import Scope
import readline

if len(sys.argv) > 1:
    parseTree = sys.argv[1] == "parseTree"
    boundTree = sys.argv[1] == "boundTree"
else:
    parseTree = False
    bndTree = False


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
continueToNextLine = False
expression = ""
indent = ""

while True:
    if bash:
        s = "$ "
    elif parseTree or bndTree:
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

    expression += new_expression

    if len(expression) == 0:
        print()
        continue

    if expression == "exit":
        exit()
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
        parseTree = not parseTree
        if parseTree:
            print("Showing Parsed Tree.")
        else:
            print("Not showing Parsed Tree.")
        expression = ""
        indent = ""
        continue
    if expression == "boundTree":
        bndTree = not bndTree
        if bndTree:
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

    if parseTree:
        rootNode.prt()
        print()
    if bndTree:
        boundTree.prt()
        print()

    if errorBag.any():
        errorBag.prt()
        errorBag.clear()
    else:
        evaluator = Evaluator(boundTree)
        print(evaluator.evaluate())
