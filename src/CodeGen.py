from bytecode import Bytecode, Instr, Label, Compare

from binder.BoundAssignmentExpression import BoundAssignmentExpression
from binder.BoundBinaryExpression import BoundBinaryExpression
from binder.BoundBlockStatement import BoundBlockStatement
from binder.BoundDeclarationExpression import BoundDeclarationExpression
from binder.BoundFunctionCall import BoundFunctionCall
from binder.BoundFunctionDeclaration import BoundFunctionDeclaration
from binder.BoundIfStatement import BoundIfStatement
from binder.BoundLiteralExpression import BoundLiteralExpression
from binder.BoundNode import BoundNode
from binder.BoundReturnStatement import BoundReturnStatement
from binder.BoundUnaryExpression import BoundUnaryExpression
from binder.BoundVariableExpression import BoundVariableExpression
from binder.BoundWhileStatement import BoundWhileStatement

from type_handling.Types import Types
from token_handling.TokenTypes import TokenTypes
from random import random as _random


class CodeGenerator:
    def __init__(self, file="<module>", name="repl"):
        self.filename = file
        self.name = name
        self.lineno = 1
        self.bytecode = Bytecode(
            [
                Instr("LOAD_CONST", None, lineno=self.lineno),
                Instr("LOAD_CONST", None, lineno=self.lineno),
                Instr("RETURN_VALUE", lineno=self.lineno),
            ]
        )

    def changeLineno(self, lineno):
        while self.bytecode[-1].lineno > lineno:
            self.bytecode.pop()

        self.lineno = lineno

        self.bytecode.extend(
            [
                Instr("PRINT_EXPR", lineno=lineno),
                Instr("LOAD_CONST", None, lineno=lineno),
                Instr("RETURN_VALUE", lineno=lineno),
            ]
        )

    def prt(self, indent=2):
        print("[")
        for i in self.bytecode:
            print(" " * indent, i, ",", sep="")
        print("]")

    def generate(self, boundTreeRoot: BoundNode, lineno: int):
        self.lineno = lineno
        self.root = boundTreeRoot
        self.bytecode.pop()
        self.bytecode.pop()
        self.bytecode.pop()
        self.bytecode.extend(
            [
                Instr("LOAD_CONST", 0, lineno=self.lineno),
                Instr("LOAD_CONST", ("random",), lineno=self.lineno),
                Instr("IMPORT_NAME", "random", lineno=self.lineno),
                Instr("IMPORT_FROM", "random", lineno=self.lineno),
                Instr("STORE_NAME", "random", lineno=self.lineno),
                Instr("POP_TOP", lineno=self.lineno),
            ]
        )
        self.bytecode.filename = self.filename
        self.bytecode.name = self.name
        self.generateFromNode(boundTreeRoot)
        self.bytecode.extend(
            [
                Instr("PRINT_EXPR", lineno=self.lineno),
                Instr("LOAD_CONST", None, lineno=self.lineno),
                Instr("RETURN_VALUE", lineno=self.lineno),
            ]
        )

        return self.bytecode.to_code()

    def generateCode(self, node: BoundBlockStatement, name="", argnames=[]):
        parentCode = self.bytecode
        self.bytecode = Bytecode()
        self.generateFromNode(node)
        self.bytecode.argcount = len(argnames)
        self.bytecode.argnames = argnames
        self.bytecode.filename = self.filename
        self.bytecode.name = name
        self.bytecode.extend(
            [
                Instr("LOAD_CONST", None, lineno=self.lineno),
                Instr("RETURN_VALUE", lineno=self.lineno),
            ]
        )
        code_obj = self.bytecode.to_code()
        self.bytecode = parentCode

        return code_obj

    def generateFromNode(self, node: BoundNode):
        if isinstance(node, BoundBlockStatement):
            self.generateBlockStatement(node)

        elif isinstance(node, BoundFunctionDeclaration):
            self.generateFunctionDeclaration(node)

        elif isinstance(node, BoundDeclarationExpression):
            self.generateDeclarationExpression(node)

        elif isinstance(node, BoundAssignmentExpression):
            self.generateAssignmentExpression(node)

        elif isinstance(node, BoundBinaryExpression):
            self.generateBinaryExpression(node)

        elif isinstance(node, BoundFunctionCall):
            self.generateFunctionCall(node)

        elif isinstance(node, BoundIfStatement):
            self.generateIfStatement(node)

        elif isinstance(node, BoundLiteralExpression):
            self.generateLiteralExpression(node)

        elif isinstance(node, BoundReturnStatement):
            self.generateReturnStatement(node)

        elif isinstance(node, BoundVariableExpression):
            self.generateVariableExpression(node)

        elif isinstance(node, BoundWhileStatement):
            self.generateWhileStatement(node)

        elif isinstance(node, BoundUnaryExpression):
            self.generateUnaryExpression(node)

    def generateBlockStatement(self, node: BoundBlockStatement):
        for statement in node.children:
            self.generateFromNode(statement)

    def generateFunctionDeclaration(self, node: BoundFunctionDeclaration):
        self.bytecode.extend(
            [
                Instr(
                    "LOAD_CONST",
                    self.generateCode(
                        node.varValue.functionBody,
                        node.varName,
                        node.varValue.str_params,
                    ),
                    lineno=self.lineno,
                ),
                Instr("LOAD_CONST", node.varName, lineno=self.lineno),
                Instr("MAKE_FUNCTION", 0, lineno=self.lineno),
                Instr("STORE_GLOBAL", node.varName, lineno=self.lineno),
                Instr("LOAD_GLOBAL", node.varName, lineno=self.lineno),
            ]
        )

    def generateDeclarationExpression(self, node: BoundDeclarationExpression):
        self.generateFromNode(node.varValue)
        self.bytecode.extend(
            [
                Instr("STORE_FAST", node.varName, lineno=self.lineno),
                Instr("LOAD_FAST", node.varName, lineno=self.lineno),
            ]
        )

    def generateAssignmentExpression(self, node: BoundAssignmentExpression):
        self.generateFromNode(node.varValue)
        self.bytecode.extend(
            [
                Instr("STORE_FAST", node.varName, lineno=self.lineno),
                Instr("LOAD_FAST", node.varName, lineno=self.lineno),
            ]
        )

    def generateBinaryExpression(self, node: BoundBinaryExpression):
        self.generateFromNode(node.left)
        self.generateFromNode(node.right)

        # Arithmetic Operators
        if node.operator.isInstance(TokenTypes.PlusOperator):
            if node.type == Types.String:
                self.bytecode.append(Instr("BUILD_STRING", 2, lineno=self.lineno))
            else:
                self.bytecode.append(Instr("BINARY_ADD", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.MinusOperator):
            self.bytecode.append(Instr("BINARY_SUBTRACT", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.StarOperator):
            self.bytecode.append(Instr("BINARY_MULTIPLY", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.SlashOperator):
            if node.type == Types.Int:
                self.bytecode.append(Instr("BINARY_FLOOR_DIVIDE", lineno=self.lineno))
            else:
                self.bytecode.append(Instr("BINARY_TRUE_DIVIDE", lineno=self.lineno))

        if node.operator.isInstance(TokenTypes.ModOperator):
            self.bytecode.append(Instr("BINARY_MODULO", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.CaretOperator):
            self.bytecode.append(Instr("BINARY_POWER", lineno=self.lineno))

        # Boolean Operators
        if node.operator.isInstance(TokenTypes.OrOperator):
            self.bytecode.append(Instr("BINARY_OR", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.AndOperator):
            self.bytecode.append(Instr("BINARY_AND", lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.NEOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.NE, lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.EEOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.EQ, lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.GEOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.GE, lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.GTOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.GT, lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.LEOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.LE, lineno=self.lineno))
        if node.operator.isInstance(TokenTypes.LTOperator):
            self.bytecode.append(Instr("COMPARE_OP", Compare.LT, lineno=self.lineno))

    def generateFunctionCall(self, node: BoundFunctionCall):
        self.bytecode.append(Instr("LOAD_GLOBAL", node.name, lineno=self.lineno))

        for c in node.paramValues:
            self.generateFromNode(c)

        self.bytecode.append(
            Instr("CALL_FUNCTION", len(node.paramValues), lineno=self.lineno)
        )

    def generateIfStatement(self, node: BoundIfStatement):
        """
        if statements

        <condition> !=> <else-label>
          <then-block>
          <goto end-label>
        <else-label>
          <else-block>
        <end-label>
        """

        elseLabel = Label()
        endLabel = Label()

        self.generateFromNode(node.condition)
        self.bytecode.append(Instr("POP_JUMP_IF_FALSE", elseLabel, lineno=self.lineno))
        self.generateFromNode(node.thenBlock)
        self.bytecode.extend(
            [Instr("JUMP_ABSOLUTE", endLabel, lineno=self.lineno), elseLabel]
        )
        self.generateFromNode(node.elseBlock)
        self.bytecode.append(endLabel)

    def generateLiteralExpression(self, node: BoundLiteralExpression):
        # TODO add support for lists
        if node.isList:
            pass
        self.bytecode.append(Instr("LOAD_CONST", node.value, lineno=self.lineno))

    def generateReturnStatement(self, node: BoundReturnStatement):
        self.generateFromNode(node.to_return)
        self.bytecode.append(Instr("RETURN_VALUE", lineno=self.lineno))

    def generateVariableExpression(self, node: BoundVariableExpression):
        self.bytecode.append(Instr("LOAD_FAST", node.name, lineno=self.lineno))

    def generateWhileStatement(self, node: BoundWhileStatement):
        """
        while Loop

        <setup-loop>
        <block-label>
          <condition> !=> <end-label>
          <block>
          <goto block-label>
        <end-label>
        """

        blockLabel = Label()
        endLabel = Label()

        self.bytecode.extend(
            [Instr("SETUP_LOOP", endLabel, lineno=self.lineno), blockLabel]
        )

        self.generateFromNode(node.condition)

        self.bytecode.append(Instr("POP_JUMP_IF_FALSE", endLabel, lineno=self.lineno))

        self.generateFromNode(node.whileBlock)

        self.extend([Instr("JUMP_ABSOLUTE", blockLabel, lineno=self.lineno), endLabel])

    def generateUnaryExpression(self, node: BoundUnaryExpression):
        self.generateFromNode(node.operand)

        if node.operator.isInstance(TokenTypes.MinusOperator):
            self.bytecode.append(Instr("UNARY_NEGATIVE", lineno=self.lineno))

        elif node.operator.isInstance(TokenTypes.NotOperator):
            self.bytecode.append(Instr("UNARY_NOT", lineno=self.lineno))
