#! /usr/bin/python3
import sys, os
from error.ErrorBag import ErrorBag
from variables.Scope import Scope
from variables.default_functions import defaultFunctions
from generateBoundTree import generateBoundTree
from executer import execute
from CodeGen import CodeGenerator

from pointers import ptr
from printing.print_color import print_color, RED

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

print("Compiling...")
errorBag.addText(text)
boundTree = generateBoundTree(text, errorBagPtr, scopePtr, path)

if errorBag.any():
    print(f"Failed\n")
    errorBag.prt()
    quit()

codeGenerator = CodeGenerator(False, module_name, file_name)

code = codeGenerator.generate(boundTree, 1)
    
print("Done.\n", "-" * os.get_terminal_size().columns, "\n", sep="")

execute(code)
