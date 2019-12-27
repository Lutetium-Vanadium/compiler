#!/usr/bin/python3
import os
import sys

from error.ErrorBag import ErrorBag
from Evaluator import Evaluator
from parser import Parser
from binder.Binder import Binder
from variables.VariableBag import VariableBag

if len(sys.argv) > 1:
    debug = sys.argv[1] == "true"
else:
    debug = False

errorBag = ErrorBag()

parser = Parser(errorBag)

bash = False
variables = VariableBag()


def dump(dct=variables, indent=2):
    print("{")
    for k, v in dct.items():
        print(" " * indent + "|" + str(k) + "|:::::   |" + str(v) + "|,")
    print("}")


while True:
    if bash:
        s = "$"
    elif debug:
        s = "┌>>"
    else:
        s = ">>>"
    print(s, end=" ")
    expression = input()

    if len(expression) == 0:
        continue

    if expression == "exit":
        exit()
    if bash:
        if expression == "repl":
            bash = False
            continue
        os.system(expression)
        continue

    if expression == "bash":
        bash = True
        continue
    if expression == "debug":
        debug = not debug
        if debug:
            print("Debugging now enabled.")
        else:
            print("Debugging now disabled.")
        continue
    if expression[0] == "$":
        os.system(expression[1:])
        continue
    if expression[0] == "#":
        eval(expression[1:])
        continue

    errorBag.addText(expression)
    rootNode, errorBag = parser.parse(expression, errorBag)
    binder = Binder(rootNode, errorBag, variables)
    boundTree, variables, errorBag = binder.bind()

    if debug:
        rootNode.prt()

    if errorBag.any():
        errorBag.prt()
        errorBag.clear()
    else:
        evaluator = Evaluator(boundTree, variables)
        print(evaluator.evaluate())
