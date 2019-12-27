from printing.print_color import print_color, LIGHT_GRAY, BRIGHT_BLUE, BRIGHT_GREEN
from token_handling.Token import Token


class Node:
    def isInstance(self, *args):
        return self.operatorToken in args

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

        if len(node.getChildren()) == 0:
            hasChildren = False
            print_color(" ", fg=LIGHT_GRAY, end="")
            print_color(node, fg=BRIGHT_GREEN)
        else:
            hasChildren = True
            print_color(node.operatorToken, fg=BRIGHT_BLUE)

        indent += "   " if isLast else "│  "

        if hasChildren:
            lastChild = node.getLastChild()

            for child in node.getChildren():
                self.prt(child, indent, child == lastChild)
