from files.focus import Focus, Group

class FocusTree:
    def __init__(self):
        self.focuses = []
        self.id = -1
        self.groups = []

    def AddFocus(self, focus):
        self.focuses.append(focus)
    def SetID(self, id):
        self.id = id
    def AddGroup(self, name, index):
        self.groups.append(Group(name, index))
    def GetLastGroupSubgroup(self, index):
        if len(self.groups) > 0:
            for i in range((len(self.groups)-1), -1, -1):
                if self.groups[i].index == index:
                    return self.groups[i]
                else:
                    return self.groups[i].SearchGroup(index)
    def GetLastGroup(self):
        return self.groups[-1]
    def GetIndexLastGroup(self, index):
        if len(self.groups) > 0:
            return self.groups[-1].SearchGroup(index)
        else:
            return self
    def HasGroup(self, index):
        if len(self.groups[-1].groups) > 0:
            return True
        else:
            return False
    def GetGroup(self, index):
       for i in range(len(self.groups)):
            if self.groups[i].index == index:
                return self.groups[i]
            else:
                return self.groups[i].SearchGroup(index)