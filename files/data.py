from files.focus_tree import FocusTree

class Data:
    def __init__(self):
        self.focus_tree = FocusTree()

    def AddFocus(self, focus):
        self.focus_tree.AddFocus(focus)