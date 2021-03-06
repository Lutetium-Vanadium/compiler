class TextSpan:
    def __init__(self, start, length):
        self.start = start
        self.end = start + length
        self.length = length

    def __len__(self):
        return self.length

    def changeEnd(self, newEnd):
        self.length = newEnd - self.start
        self.end = newEnd
