import xml.etree.ElementTree as ET
import sys


filename = sys.argv[1]
myTree = ET.parse("output.xml")
root = myTree.getroot()
locs = root.findall(".//location")
parent_map = {c:p for p in root.iter() for c in p}

for loc in locs:
    if loc.attrib['value'][:2+len(filename)] != "["+filename+"]":
        parent = parent_map[loc]
        grandpa = parent_map[parent]
        grandpa.remove(parent)

myTree.write("output_rectified.xml")


