from unittest import TestCase
import os, sys

sys.path.append("/".join(os.getcwd().split("/")[:-1]))
sys.path.append("/".join(os.getcwd().split("/")[:-1]) + "/src")
sys.path.append(os.getcwd() + "/src")
from src.parser import Parser
from src.Evaluator import Evaluator
from src.binder.Binder import Binder
from src.error.ErrorBag import ErrorBag
from src.variables.Scope import Scope


def run_expression(text):
    scope = Scope()
    errorBag = ErrorBag()
    parser = Parser(errorBag)
    errorBag.addText(text)
    rootNode, errorBag = parser.parse(text, errorBag)
    binder = Binder(rootNode, errorBag, scope)
    boundTree, scope, errorBag = binder.bind()

    if errorBag.any():
        return None
    else:
        evaluator = Evaluator(boundTree, scope)
        return evaluator.evaluate()


class TestOperations(TestCase):
    def test_arithmetic(self):
        self.assertEqual(run_expression("1+1"), 2)
        self.assertEqual(run_expression("387-23"), 364)
        self.assertEqual(run_expression("23*3"), 69)
        self.assertEqual(run_expression("23 / 6"), 3)
        self.assertEqual(run_expression("3^4"), 81)
        self.assertAlmostEqual(run_expression("23.0 / 6"), 23 / 6)

    def test_boolean(self):
        self.assertEqual(run_expression("true || true"), True)
        self.assertEqual(run_expression("true || false"), True)
        self.assertEqual(run_expression("false || true"), True)
        self.assertEqual(run_expression("false || false"), False)

        self.assertEqual(run_expression("true && true"), True)
        self.assertEqual(run_expression("true && false"), False)
        self.assertEqual(run_expression("false && true"), False)
        self.assertEqual(run_expression("false && false"), False)

        self.assertEqual(run_expression("!true"), False)
        self.assertEqual(run_expression("!false"), True)

        self.assertEqual(run_expression("23 > 1"), True)
        self.assertEqual(run_expression("2 > 12"), False)

        self.assertEqual(run_expression("23 < 1"), False)
        self.assertEqual(run_expression("2 < 12"), True)

        self.assertEqual(run_expression("23 >= 1"), True)
        self.assertEqual(run_expression("2 >= 12"), False)
        self.assertEqual(run_expression("12 >= 12"), True)

        self.assertEqual(run_expression("23 <= 1"), False)
        self.assertEqual(run_expression("2 <= 12"), True)
        self.assertEqual(run_expression("12 <= 12"), True)

        self.assertEqual(run_expression("12 != 12"), False)
        self.assertEqual(run_expression("32 != 12"), True)

        self.assertEqual(run_expression("12 == 12"), True)
        self.assertEqual(run_expression("12 == 42"), False)
