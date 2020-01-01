from unittest import TestCase
import os, sys

sys.path.append(os.getcwd() + "/src")
sys.path.append("/".join(os.getcwd().split("/")[:-1]))
sys.path.append("/".join(os.getcwd().split("/")[:-1]) + "/src")

from tests.helpers import *


class TestFunctions(TestCase):
    def test_inbuilt(self):
        self.assertEqual(run_expression("min(1231, 123123)", "int"), 1231)
        self.assertEqual(run_expression("min(1231231, 123123)", "int"), 123123)
        self.assertEqual(run_expression("min(1231231, 1231231)", "int"), 1231231)
        self.assertEqual(
            run_expression("min(min(125143, 123132), 123153)", "int"), 123132
        )

        self.assertEqual(run_expression("max(1231, 123123)", "int"), 123123)
        self.assertEqual(run_expression("max(1231231, 123123)", "int"), 1231231)
        self.assertEqual(run_expression("max(1231231, 1231231)", "int"), 1231231)
        self.assertEqual(
            run_expression("max(max(125143, 129132), 123153)", "int"), 129132
        )

