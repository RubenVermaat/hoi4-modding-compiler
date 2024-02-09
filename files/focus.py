class Focus:
    def __init__(self, id):
        self.id = id
        self.arguments = []
        self.groups = []

    def GetID(self):
        return self.id
    def AddArgument(self, type, value):
        self.arguments.append(Argument(type, value))
    def AddGroup(self, group):
        self.groups.append(group)

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