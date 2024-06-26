import functions.focus_tree
import re
import os
from files.data import Data
from files.focus import Focus, Argument, Group
from files.focus_tree import FocusTree

file = open(r"C:\Users\ruben\Documents\Paradox Interactive\Hearts of Iron IV\mod\Compiler-mod\gondor.txt", "r")
data = Data()
creating = 0
group = None
focus = None
focus_tree = FocusTree()
indents = 0
typeRegex = '[^a-zA-Z0-9_]'
valueRegex = '[^a-zA-Z0-9_.-]'
commandRegex = '[^a-zA-Z0-9_#]'
for line in file.readlines():
    if re.sub(commandRegex, '', line).startswith("#") == False:
        if line.startswith("continuous_focus_position"):
            values = line[line.index('(')+1:line.index(')')]
            focus_tree.continuous_focus_x = values[0:values.index(',')]
            focus_tree.continuous_focus_y = values[values.index(',')+1:len(values)]
        else:
            if line.startswith("focus"):
                tempName = re.sub(typeRegex, '', line[0:line.index(':')])
                indents = 0
                focus_tree.AddGroup(tempName, indents)   
            elif line.find(":") != -1:
                #Its a group
                tempName = re.sub(typeRegex, '', line[0:line.index(':')])
                if focus_tree.groups != []:
                    if line.count("\t") < indents:
                        indents = line.count("\t")
                        focus_tree.GetLastGroup().AddGroup(tempName, indents)
                    elif line.count("\t") > indents: #Group in a group
                        focus_tree.GetLastGroupSubgroup(indents).AddGroup(tempName, (indents+1))
                    elif line.count("\t") == indents:
                        focus_tree.GetIndexLastGroup((indents-1)).AddGroup(tempName, indents)
            elif line.find("=") != -1:
                #Its a single argument and value
                if (line.count("\t") != 0):
                    type = re.sub(typeRegex, '', line[0:line.index('=')])
                    value = re.sub(valueRegex, '', line[line.index('=')+1:len(line)])
                    indents = line.count("\t")
                    focus_tree.GetIndexLastGroup((indents-1)).AddArgument(Argument(type, value))
                else:
                    type = re.sub(typeRegex, '', line[0:line.index('=')])
                    value = re.sub(valueRegex, '', line[line.index('=')+1:len(line)])
                    focus_tree.AddArgument(Argument(type, value))
            elif len(re.sub(valueRegex, '', line)) > 0:
                #Its a single value
                type = "SingeValue"
                value = re.sub(valueRegex, '', line)
                indents = line.count("\t")
                    
                focus_tree.GetIndexLastGroup((indents-1)).AddArgument(Argument(type, value))
                #focus_tree.GetLastGroup().AddArgument(Argument(type, value))
    else: 
        if focus != None:
            print(line[1:len(line)])
file.close()

def recursive_loop(f, item):
    indents = ""
    for i in range(item.index):
        indents = indents + "\t"
    f.write(indents + item.name + " = {\n")
    if len(item.arguments) > 0:
        for argument in item.arguments:
            f.write(indents + "\t" + WriteArgument(argument) + "\n")
    if len(item.groups) > 0:
        for group in item.groups:
            recursive_loop(f, group)
        f.write(indents + "}\n")
    else:
        f.write(indents + "}\n")
        indents = indents[:-2]
    

def WriteArgument(argument):
    if argument.type == "prerequisite":
        return argument.type + " { focus = " + argument.value + " }"
    elif argument.type == "SingeValue":
        return argument.value
    else:
        return argument.type + " = " + argument.value

file_path = 'example.txt'
os.remove(file_path)
with open(file_path, 'w') as f:
    f.write("continuous_focus_position = {\n")
    f.write("\tx = " + focus_tree.continuous_focus_x + "\n")
    f.write("\ty = " + focus_tree.continuous_focus_y + "\n")
    f.write("}\n")
    for argument in focus_tree.arguments:
        f.write(WriteArgument(argument) + "\n")
    for group in focus_tree.groups:
        recursive_loop(f, group)

# ### Getting the id name from the line
# result = line.replace("id","")
# result = result.replace("=","")
# result = re.sub(r'[^a-zA-Z0-9]', '', result)
# ### Creating focus with that id
# focus = Focus(result)