from unittest import TestCase
import os, sys

sys.path.append(os.getcwd() + "/src")
from src.parser import Parser
from src.Evaluator import Evaluator
from src.binder.Binder import Binder
from src.error.ErrorBag import ErrorBag
from src.variables.Scope import Scope


def run_multiple_expressions(txt_lst, expected_type, returnType="single"):
    """
    txt_lst: List of commands to run
    expected_type: [int, bool, float]
    returnType: Gives return type
            - single: returns last element
            - all: returns the full list 
    """
    scope = Scope()
    errorBag = ErrorBag()
    parser = Parser(errorBag)
    output_lst = []
    for text in txt_lst:
        errorBag.addText(text)
        _, rootNode, errorBag = parser.parse(text, errorBag)
        binder = Binder(rootNode, errorBag, scope)
        boundTree, scope, errorBag = binder.bind()

        if errorBag.any():
            output_lst.append(None)
        else:
            evaluator = Evaluator(boundTree)
            e = str(evaluator.evaluate())
            if expected_type == "int":
                e = int(e)
            elif expected_type == "float":
                e = float(e)
            elif expected_type == "bool":
                e = e == "True"

            output_lst.append(e)
    if returnType == "single":
        return output_lst[-1]
    elif returnType == "all":
        return output_lst


def run_expression(text, expected_type):
    return run_multiple_expressions([text], expected_type)


class TestOperations(TestCase):
    def test_arithmetic(self):
        self.assertEqual(run_expression("1+1", "int"), 2)
        self.assertEqual(run_expression("387-23", "int"), 364)
        self.assertEqual(run_expression("23*3", "int"), 69)
        self.assertEqual(run_expression("23 / 6", "int"), 3)
        self.assertEqual(run_expression("3^4", "int"), 81)
        self.assertAlmostEqual(run_expression("23.0 / 6", "float"), 23 / 6)

        self.assertEqual(run_expression("12 + 23 - ((23 * 56 / 12)%7)^3", "int"), 27)
        self.assertEqual(run_expression("32 * 23 + 223 - (2 - 24 * 2)/27", "int"), 961)
        self.assertEqual(run_expression("23^2 - 212*23 +(213 - 1 * 231)", "int"), -4365)
        self.assertAlmostEqual(run_expression("23.4 * (23 + 12)/2.1", "float"), 390.0)
        self.assertAlmostEqual(
            run_expression("23^2 - 212.4/23 +(213 - 1.7/23)", "float"),
            23 ** 2 - 212.4 / 23 + (213 - 1.7 / 23),
        )
        self.assertAlmostEqual(
            run_expression("32 * 23 + 223 - (2 - 24.0 * 2)/27", "float"),
            (32 * 23 + 223 - (2 - 24 * 2) / 27),
        )

    def test_boolean(self):
        self.assertEqual(run_expression("true || true", "bool"), True)
        self.assertEqual(run_expression("true || false", "bool"), True)
        self.assertEqual(run_expression("false || true", "bool"), True)
        self.assertEqual(run_expression("false || false", "bool"), False)

        self.assertEqual(run_expression("true && true", "bool"), True)
        self.assertEqual(run_expression("true && false", "bool"), False)
        self.assertEqual(run_expression("false && true", "bool"), False)
        self.assertEqual(run_expression("false && false", "bool"), False)

        self.assertEqual(run_expression("!true", "bool"), False)
        self.assertEqual(run_expression("!false", "bool"), True)

        self.assertEqual(run_expression("true && (true || false)", "bool"), True)
        self.assertEqual(run_expression("false || true && (!true)", "bool"), False)
        self.assertEqual(run_expression("true && (!true || false)", "bool"), False)
        self.assertEqual(
            run_expression("(false && true) || (!false || !true)", "bool"), True
        )

        self.assertEqual(run_expression("23 > 1", "bool"), True)
        self.assertEqual(run_expression("2 > 12", "bool"), False)

        self.assertEqual(run_expression("23 < 1", "bool"), False)
        self.assertEqual(run_expression("2 < 12", "bool"), True)

        self.assertEqual(run_expression("23 >= 1", "bool"), True)
        self.assertEqual(run_expression("2 >= 12", "bool"), False)
        self.assertEqual(run_expression("12 >= 12", "bool"), True)

        self.assertEqual(run_expression("23 <= 1", "bool"), False)
        self.assertEqual(run_expression("2 <= 12", "bool"), True)
        self.assertEqual(run_expression("12 <= 12", "bool"), True)

        self.assertEqual(run_expression("12 != 12", "bool"), False)
        self.assertEqual(run_expression("32 != 12", "bool"), True)

        self.assertEqual(run_expression("12 == 12", "bool"), True)
        self.assertEqual(run_expression("12 == 42", "bool"), False)

    def test_variables(self):
        self.assertEqual(run_expression("int a = 2", "int"), 2)
        self.assertEqual(run_expression("var a = 2", "int"), 2)
        self.assertEqual(run_expression("const a = 2", "int"), 2)
        self.assertEqual(run_expression("float a = 2.0", "float"), 2.0)
        self.assertEqual(run_expression("bool a = false", "bool"), False)

        self.assertEqual(
            run_multiple_expressions(["var a = true", "!a"], "bool"), False
        )

        self.assertEqual(
            run_multiple_expressions(["var a = false", "!a"], "bool"), True
        )

        to_run = [
            "bool a = true",
            "bool b = false",
            "a || a",
            "a || b",
            "b || a",
            "b || b",
            "a && a",
            "a && b",
            "b && a",
            "b && b",
            "a &&= false",
            "b ||= true",
            "a == b",
        ]

        expected_output = [
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            False,
        ]
        self.assertEqual(
            run_multiple_expressions(to_run, "bool", "all"), expected_output
        )

        to_run = [
            "int a = 23",
            "a += 46",
            "int b = 41",
            "b -= 12",
            "int c = 13",
            "c *= 11",
            "int d = 23",
            "d /= 7",
            "int e = 23",
            "e %= 7",
        ]

        length = len(to_run)

        expected_output = [23, 69, 41, 29, 13, 143, 23, 3, 23, 2]

        self.assertEqual(
            run_multiple_expressions(to_run, "int", "all"), expected_output
        )

    def test_scoping(self):
        to_test = """\
            int a = 23
            {
                a += 27
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 50)

        to_test = """\
            int a = 23
            {
                a += 27
            }
            a
        """
        self.assertEqual(run_expression(to_test, "int"), 50)

        to_test = """\
            int a = 23
            {
                int a = 4
                a + 4
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 8)

        to_test = """\
            int a = 23
            {
                bool a = true
                a && true
            }
        """
        self.assertEqual(run_expression(to_test, "bool"), True)

        to_test = """\
            int a = 23
            {
                bool a = true
            }
            a
        """
        self.assertEqual(run_expression(to_test, "int"), 23)

        to_test = """\
            int a = 23
            {
                int a = 75
                {
                    a += 23
                }
                a
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 98)

        to_test = """\
            if true {
                1
            } else {
                2
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 1)

    def test_scoping(self):
        to_test = """\
            if true {
                1
            } else if true {
                2
            } else {
                3
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 1)

        to_test = """\
            if true {
                1
            } else {
                2
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 1)

        to_test = """\
            if false {
                1
            } else {
                2
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 2)

        to_test = """\
            if false {
                1
            } else if true {
                2
            } else {
                3
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 2)

        to_test = """\
            if false {
                1
            } else if false {
                2
            } else {
                3
            }
        """
        self.assertEqual(run_expression(to_test, "int"), 3)

    def test_loops(self):
        to_run = ["int r = 0", "for i in range(11) { r += i }", "r"]
        self.assertEqual(run_multiple_expressions(to_run, "int"), 55)

        to_run = ["int r = 0", "int i = 1", "while (i <= 100){ r += i  i += 1 }", "r"]
        self.assertEqual(run_multiple_expressions(to_run, "int"), 5050)

        to_run = ["int a = 1", "int c = 0", "while a < 1024 { a *= 2  c += 1 }", "c"]
        self.assertEqual(run_multiple_expressions(to_run, "int"), 10)
