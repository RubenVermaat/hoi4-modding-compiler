class Focus:
    def __init__(self, id):
        self.id = id
        self.arguments = []
        self.groups = []
        self.comments = []

    def GetID(self):
        return self.id
    def AddArgument(self, type, value):
        self.arguments.append(Argument(type, value))
    def AddGroup(self, group):
        self.groups.append(group)
    def AddComment(self, comment):
        self.comments.append(comment)

class Argument():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Group():
    def __init__(self, name):
        self.name = name
        self.arguments = []
    def AddArgument(self, argument):
        self.arguments.append(argument)