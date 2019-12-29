from syntax_tree.AssignmentNode import AssignmentNode
from syntax_tree.BinaryNode import BinaryOperatorNode
from syntax_tree.BlockStatement import BlockStatement
from syntax_tree.DeclarationNode import DeclarationNode
from syntax_tree.ExpressionNode import ExpressionNode
from syntax_tree.WhileStatement import WhileStatement
from syntax_tree.UnaryNode import UnaryOperatorNode

from token_handling.TokenTypes import TokenTypes
from token_handling.Token import Token


def constructForStatement(variable, upperBound, forBlock):
    # TODO implement For properly, needed FUNCTIONS, (for 'range')

    # declaring the variable
    assignmentToken = Token("=", TokenTypes.AssignmentOperator, -1)
    declarationToken = Token(
        "int", TokenTypes.DeclarationKeyword, variable.text_span.start
    )
    numberToken = Token(0, TokenTypes.Number, upperBound.text_span.start)

    expression = ExpressionNode(numberToken)
    assignmentNode = AssignmentNode(variable, expression, assignmentToken)
    variableStatement = DeclarationNode(declarationToken, assignmentNode)

    # creating the while statement
    ltToken = Token("<", TokenTypes.LTOperator, -1)
    operatorToken = Token("++", TokenTypes.PlusPlusOperator, -1)
    whileToken = Token("while", TokenTypes.WhileKeyword, -1)

    condition = BinaryOperatorNode(variable, upperBound, ltToken)
    variable_increment = UnaryOperatorNode(variable, operatorToken)
    forBlock.add(variable_increment)
    whileStatement = WhileStatement(whileToken, condition, forBlock)

    return BlockStatement([variableStatement, whileStatement])
