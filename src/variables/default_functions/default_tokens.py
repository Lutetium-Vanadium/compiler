from token_handling.Token import Token
from token_handling.TokenTypes import TokenTypes
from textSpan import TextSpan

ifToken = Token("if", TokenTypes.IfKeyword, -1)
LTToken = Token("<", TokenTypes.LTOperator, -1)
GTToken = Token(">", TokenTypes.GTOperator, -1)
returnToken = Token("return", TokenTypes.ReturnKeyword, -1)

textSpan = TextSpan(-1, 0)
