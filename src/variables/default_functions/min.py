from variables.FunctionVariable import FunctionVariable
from variables.Variable import Variable
from variables.default_functions.default_tokens import ifToken, LTToken, returnToken

from syntax_tree.BinaryNode import BinaryOperatorNode
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.IfStatement import IfStatement
from syntax_tree.ReturnStatement import ReturnStatement

from type_handling.Types import Types
from token_handling.Token import Token
from token_handling.TokenTypes import TokenTypes

name = "min"
data_type = Types.Int
params = [Variable("a", Types.Int), Variable("b", Types.Int)]

paramA = ExpressionNode(Token("a", TokenTypes.Variable, -1))
paramB = ExpressionNode(Token("b", TokenTypes.Variable, -1))
# If statement
condition = BinaryOperatorNode(paramA, paramB, LTToken)

returnA = ReturnStatement(returnToken, paramA)
thenBlock = BlockStatement([returnA])

returnB = ReturnStatement(returnToken, paramB)
elseBlock = BlockStatement([returnB])

ifStatement = IfStatement(ifToken, condition, thenBlock, elseBlock)

min_func = FunctionVariable(name, Types.Int, params, BlockStatement([ifStatement]))
