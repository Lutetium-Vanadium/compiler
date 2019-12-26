#!/usr/bin/python3
import os
import sys
from parser import Parser
from error.ErrorBag import ErrorBag

if len(sys.argv) > 1:
    debug = sys.argv[1] == "true"
else:
    debug = False

errorBag = ErrorBag()

parser = Parser(errorBag)

bash = False

variables = {}


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

    variables, val = parser.parse(expression, variables)

    if debug:
        val.prt()

    if errorBag.any():
        errorBag.prt()
        errorBag.clear()
    else:
        print(val.evaluate())
