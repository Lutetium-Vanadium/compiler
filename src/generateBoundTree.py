from syntax_tree.lexer import Lexer
from syntax_tree.parser import Parser
from binder.Binder import Binder

from pointers import ptrVal


def generateBoundTree(text, errorBagPtr, scopePtr, path):
    # Initializing the APIs
    lexer = Lexer(errorBagPtr)
    parser = Parser(errorBagPtr)
    binder = Binder(errorBagPtr, scopePtr, path)

    tokenList = lexer.lex(text)[1]
    rootNode = parser.parse(tokenList)

    return binder.bind(rootNode)
