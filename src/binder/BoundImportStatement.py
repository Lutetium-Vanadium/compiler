from binder.BoundNode import BoundNode
from type_handling.Types import Types
from error.ErrorBag import ErrorBag
from pointers import ptr

import os

class BoundImportStatement(BoundNode):
    def __init__(self, filePath, text_span, scopePtr, curpath):
        self.filePath = filePath
        self.text_span = text_span
        self.type = Types.Void

        # Imported here to avoid circular imports:
        # generateBoundTree requires Binder
        # Binder requires this
        # And this requires generateBoundTree
        from generateBoundTree import generateBoundTree
        path = os.path.join(curpath, filePath.value)

        text = ""
        with open(path, "r") as f:
            text = f.read()

        self.errorBag = ErrorBag(text=text)
        errorBagPtr = ptr(self.errorBag)

        self.boundTree = generateBoundTree(text, errorBagPtr, scopePtr, path)

    def __repr__(self):
        return f"import {self.filePath}"

    def __repr__(self):
        return f"import {self.filePath}"

    def get_children(self):
        return [self.filePath]

    def get_txt(self):
        return f"BoundImportStatement"
