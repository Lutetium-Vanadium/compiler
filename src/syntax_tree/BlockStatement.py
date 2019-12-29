from syntax_tree.Node import Node
from textSpan import TextSpan


class BlockStatement(Node):
    def __init__(self, statement_lst):
        self.statement_lst = statement_lst
        if len(statement_lst) > 0:
            start = statement_lst[0].text_span.start
            end = statement_lst[-1].text_span.end
        else:
            start = -1
            end = -1
        self.text_span = TextSpan(start, end - start)

    def __repr__(self):
        s = f"Block: length = {len(self.statement_lst)}"
        for i in statement_lst:
            s += f"\n{i}"
        return s

    def __str__(self):
        s = f"Block: length = {len(self.statement_lst)}"
        for i in statement_lst:
            s += f"\n{i}"
        return s

    def add(self, *args):
        self.statement_lst.extend(args)
        newEnd = self.statement_lst[-1].text_span.end
        self.text_span.changeEnd(newEnd)

    def getChildren(self):
        return self.statement_lst

    def get_txt(self):
        return "Block Statement"
