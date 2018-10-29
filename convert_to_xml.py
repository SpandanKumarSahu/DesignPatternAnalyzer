from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

i = 0


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def count_spaces(line):
    count = 0
    for i in line:
        if i == " ":
            count += 1
        else:
            return count


def parse(str):
    ele= str[:str.index(":")].split()
    ele_mod = ""
    for e in ele:
        ele_mod += e+"_"
    ele_mod = ele_mod[:-1] if len(ele) > 0 else ele_mod
    if len(str[str.index(":") + 1:].strip()) == 0:
        val = {}
    elif str[str.index(":")+1:].strip()[0] == "'":
        val = {"value": str[str.index(":")+1:].strip()[1:-1]}
    else:
        val = {"value": str[str.index(":") + 1:].strip()}
    return ele_mod, val


def recfunc(parent, level):
    global i
    while i < len(data):
        str, index = data[i]
        if index == level:
            ele, val = parse(str)
            child = SubElement(parent, ele, val)
            i += 1
        elif index > level:
            recfunc(child, index)
        else:
            return

with open("output.txt", "r") as f:
    data = f.readlines()
    data = [(x.strip(), count_spaces(x)) for x in data if x != "\n"]
#    data = data[:120]
root = Element('root')
recfunc(root, 0)


# print(tostring(root))
print(prettify(root))
