from printing.print_color import print_color, LIGHT_GRAY
from token_handling.Token import Token


class Node:
    def getLastChild(self):
        children = self.getChildren()
        if isinstance(children, (tuple, list)):
            return children[-1]

        else:
            return children

    def prt(self, node=None, indent="", isLast=True):
        if node == None:
            node = self

        marker = "└──" if isLast else "├──"

        print_color(indent, fg=LIGHT_GRAY, end="")
        print_color(marker, fg=LIGHT_GRAY, end="")

        if isinstance(node, Token):
            isNode = False
            print_color(" ", fg=LIGHT_GRAY, end="")
            print_color(node, fg=LIGHT_GRAY, end="")
        else:
            isNode = True
            print_color(node.operatorToken, fg=LIGHT_GRAY, end="")

        print()

        indent += "   " if isLast else "│  "

        if isNode:
            lastChild = node.getLastChild()

            for child in node.getChildren():
                self.prt(child, indent, child == lastChild)
