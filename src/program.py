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
from printing.print_color import print_color, RED

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
    while i < len(s) and (s[i] == "\t" or s[i] == " "):
        i += 1
    return s[:i]


def prt_help():
    print("Help menu for REPL:")
    print(
        """\
    Commands:
        bash - runs all commands as system commands.
        boundTree - Shows the bound tree.
        bytecode - Shows the bytecode instructions generated.
        exit - Exits out of the repl.
        help - Shows this help menu
        parseTree - Shows the parsed tree.
        repl - returns to repl from bash mode.
    
    Pre-Command Characters:
        '$' - Runs this command as bash.
        '#' - Runs this command as internal python code.
    """
    )
    # setLineNo {int line} - Sets the current line number to the given number.
    # -- All code written in the lines from {line} to current line number will no longer exist
    #     and hence all variables and functions declared will no longer exist --


errorBag = ErrorBag()
errorBagPtr = ptr(errorBag)

globalScope = Scope()
globalScope.addRange(defaultFunctions)
globalScopePtr = ptr(globalScope)

lexer = Lexer(errorBagPtr)
parser = Parser(errorBagPtr)
binder = Binder(errorBagPtr, globalScopePtr)
evaluator = Evaluator(errorBagPtr)
codeGenerator = CodeGenerator()

bash = False
continueToNextLine = False
expression = ""
indent = ""
lineno = 1

while True:
    s = f"[{lineno}]: "
    if bash:
        s = "$ "
    if continueToNextLine:
        if showParseTree or showBoundTree or showBytecode:
            s = "├·· "
        else:
            s = "··· "
    new_expression = cmd_input(s, indent)

    if continueToNextLine:
        indent = getIndent(new_expression)
        new_expression = new_expression.lstrip()

    expression += indent + new_expression

    if len(expression) == 0:
        print()
        continue

    command = expression.strip().split()[0]
    args = expression.strip().split()[1:]

    if command == "exit":
        break
    if command == "help":
        prt_help()
        expression = ""
        indent = ""
        continue
    # if command == "setLineNo":
    #     if len(args):
    #         if args[0].isdigit():
    #             new_lineno = int(args[0])
    #             if new_lineno < lineno:
    #                 lineno = new_lineno
    #                 codeGenerator.changeLineno(new_lineno)
    #             else:
    #                 print_color(
    #                     "\nNew line number must be less than the current line number.\n",
    #                     fg=RED,
    #                 )
    #         else:
    #             print_color("\nYou can only set line number to an integer.\n", fg=RED)
    #     else:
    #         print_color("\nYou need to give a line number.\n", fg=RED)
    #     expression = ""
    #     indent = ""
    #     continue
    if bash:
        if command == "repl":
            bash = False
            expression = ""
            indent = ""
            continue
        os.system(expression)
        expression = ""
        indent = ""
        continue

    if command == "bash":
        bash = True
        expression = ""
        indent = ""
        continue
    if command == "parseTree":
        showParseTree = not showParseTree
        if showParseTree:
            print("Showing Parsed Tree.")
        else:
            print("Not showing Parsed Tree.")
        expression = ""
        indent = ""
        continue
    if command == "boundTree":
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
    errorBag.line_num = lineno
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

        val = evaluator.evaluate(boundTree)
        if val != None:
            print(val)
