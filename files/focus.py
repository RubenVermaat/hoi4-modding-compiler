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
    def __init__(self, name, index):
        self.name = name
        self.arguments = []
        self.groups = []
        self.index = index
    def AddArgument(self, argument):
        self.arguments.append(argument)
    def AddGroup(self, name, index):
        self.groups.append(Group(name, index))
    def SearchGroup(self, index):
        if self.index == index:
            return self
        if len(self.groups) > 0:
            for i in range((len(self.groups)-1), -1, -1):
                if self.groups[i].index == index:
                    return self.groups[i]
                else:
                    return self.groups[i].SearchGroup(index)
