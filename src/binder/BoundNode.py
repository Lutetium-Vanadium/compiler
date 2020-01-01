from printing.print_color import print_color, LIGHT_GRAY, BRIGHT_BLUE, BRIGHT_GREEN
from token_handling.Token import Token


class BoundNode:
    def get_children(self):
        return []

    def getLastChild(self):
        return self.get_children()[-1]

    def prt(self, node, indent="", isLast=True):
        marker = "└──" if isLast else "├──"

        print_color(indent, fg=LIGHT_GRAY, end="")
        print_color(marker, fg=LIGHT_GRAY, end="")

        if len(node.get_children()) == 0:
            hasChildren = False
            print_color(" ", fg=LIGHT_GRAY, end="")
            print_color(node.get_txt(), fg=BRIGHT_GREEN)
        else:
            hasChildren = True
            print_color(node.get_txt(), fg=BRIGHT_BLUE)

        indent += "   " if isLast else "│  "

        if hasChildren:
            lastChild = node.getLastChild()

            for child in node.get_children():
                self.prt(child, indent, child == lastChild)
