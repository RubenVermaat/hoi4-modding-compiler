import functions.focus_tree
import re
import os
from files.data import Data
from files.focus import Focus, Argument, Group

file = open(r"C:\Users\ruben\Documents\Paradox Interactive\Hearts of Iron IV\mod\Compiler-mod\gondor.txt", "r")
data = Data()
creating = 0
group = None
focus = None
typeRegex = '[^a-zA-Z0-9_]'
valueRegex = '[^a-zA-Z0-9_]'
for line in file.readlines():
    if line.startswith("#") == False:
        ### Defining what it is creating
        if creating == 0:
            if line.startswith("focus_tree"):
                print("nothing")
        elif creating == 1:
            if line.startswith("\t"):
                creating = 2
        elif creating == 2: #Creating focus
            if line.find("\t") == -1:
                creating = 1
                data.AddFocus(focus)
            if line.startswith("\t\t"):
                creating = 3
        elif creating == 3: #Creating group
            if line.startswith("\t\t") == False:
                creating = 2
                focus.AddGroup(group)
        
        ### Creating that
        if creating == 1:
            print("")
        if creating == 2:
            if line.startswith("\t"): #Checking for indent
                if line.find("=") != -1:
                    type = re.sub(typeRegex, '', line[0:line.index('=')])
                    value = re.sub(valueRegex, '', line[line.index('=')+1:len(line)])
                    if type == "id":
                        focus = Focus(value)
                    else:
                        focus.AddArgument(type, value)
                elif line.find(":") != -1:
                    name = re.sub(typeRegex, '', line[0:line.index(':')])
                    creating = 2
                    group = Group(name)
        elif creating == 3:
            if line.startswith("\t\t"):
                if line.find("=") != -1:
                    type = re.sub(typeRegex, '', line[0:line.index('=')])
                    value = re.sub(valueRegex, '', line[line.index('=')+1:len(line)])
                else:
                    type = "SingleArgument"
                    value = re.sub(valueRegex, '', line)
                group.AddArgument(Argument(type, value))
        if line.startswith("focus:"):
            creating = 1
    else: 
        if focus != None:
            focus.AddComment(line[1:len(line)])
file.close()

def WriteArgument(argument):
    if argument.type == "prerequisite":
        return argument.type + " { focus = " + argument.value + " }"
    elif argument.type == "SingleArgument":
        return argument.value
    else:
        return argument.type + " = " + argument.value

file_path = 'example.txt'
os.remove(file_path)
# Open a file in write mode
with open(file_path, 'w') as f:
    for focus in data.focus_tree.focuses:
        for comment in focus.comments:
            f.write("#" + comment)
        f.write("focus = {\n")
        f.write("\tid = " + focus.GetID() + "\n")
        for group in focus.groups:
            f.write("\t" + group.name + " = {\n")
            for argument in group.arguments:
                f.write("\t\t" + WriteArgument(argument) + "\n")
            f.write("\t}\n")
        for argument in focus.arguments:
            f.write("\t" + WriteArgument(argument) + "\n")
        f.write("}\n")


# ### Getting the id name from the line
# result = line.replace("id","")
# result = result.replace("=","")
# result = re.sub(r'[^a-zA-Z0-9]', '', result)
# ### Creating focus with that id
# focus = Focus(result)