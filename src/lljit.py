#! /usr/bin/python3
import sys, os
from error.ErrorBag import ErrorBag
from variables.Scope import Scope
from variables.default_functions import defaultFunctions
from syntax_tree.lexer import Lexer
from syntax_tree.parser import Parser
from binder.Binder import Binder
from CodeGen import CodeGenerator
from executer import execute

from pointers import ptr
from printing.print_color import print_color, RED
from dis import disassemble

if len(sys.argv) <= 1:
    print_color("\nYou need to input a file name\n", fg=RED)
    quit()

path = os.path.join(os.getcwd(), sys.argv[1])
split_path = path.split("/")
module_name = split_path[-2]
file_name = split_path[-1]

text = ""
with open(path, "r") as f:
    text = f.read()

# Initializing the error handling
errorBag = ErrorBag()
errorBagPtr = ptr(errorBag)

# Initializing the scope
scope = Scope()
scope.addRange(defaultFunctions)
scopePtr = ptr(scope)

# Initializing the APIs
lexer = Lexer(errorBagPtr)
parser = Parser(errorBagPtr)
binder = Binder(errorBagPtr, scopePtr)
codeGenerator = CodeGenerator(False, module_name, file_name)

errorBag.addText(text)

print("Compiling...")
tokenList = lexer.lex(text)[1]
rootNode = parser.parse(tokenList)
boundTree = binder.bind(rootNode)

if errorBag.any():
    print("Failed\n")
    errorBag.prt()
    quit()

code = codeGenerator.generate(boundTree, 1)

print("Done.\n\n", "-" * os.get_terminal_size().columns, "\n", sep="")

execute(code)
