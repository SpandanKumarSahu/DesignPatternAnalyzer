import xml.etree.ElementTree as ET

def get_access_level(c):
    access_level_dict = {}
    level = ""
    for child in c:
        if child.tag == "public" or child.tag == "private" or child.tag == "protected":
            level = child.tag
            continue
        if len(level) > 0:
            access_level_dict[child] = level
    return access_level_dict


def is_variable_static(node):
    str = node.find("location").attrib['value']
    filename = str[str.find("[")+1: str.find("]")]
    loc = int(str[str.find(":")+1:])
    with open(filename, "r") as f:
        data = f.readlines()
    line = data[loc-1]
    if "static" in line:
        return 1
    else:
        return 0


def is_class_interface(c):
    funcs = c.findall(".//member_function_t")
    for func in funcs:
        is_virtual = (func.find("virtual").attrib['value'] == "pure virtual")
        if is_virtual:
            return 1
    return 0

# TODO:
# 1. Check in the function body if they actually use the derived classes.

def is_choosing_in_interface(i_node, ns_tag):
    static_funcs = i_node.findall(".//member_function_t")
    for func in static_funcs:
        if func.find("is_static").attrib['value'] == "True" and \
                        func.find("return_type").attrib['value'].split()[0].find(i_node.attrib['value']) != -1:
            # Get derived classes
            derived_classes = i_node.find("derived_classes").findall("class")
            if len(derived_classes) == 0:
                return 0
            # derived_classes_tags = [x.attrib['value'][len(ns_tag)+1:].split()[0] for x in derived_classes]
            return 1
    return 0


def check_singleton_pattern(c, access_level):
    # Check class has a private static object of itself
    private_variables = [x for x in access_level if access_level[x] == "private" and x in c.findall(".//variable_t")]
    count = 0
    for x in private_variables:
        type_t = x.find("type")
        is_static = is_variable_static(x)
        if type_t.attrib['value'].find(c.attrib['value']) != -1 and is_static:
            count += 1
    if count == 0:
        return 0

    # Check if all the constructors are private
    cons = c.findall("constructors_t")
    for con in cons:
        if access_level[con] != "private":
            return 0

    # Check if all the destructors are private
    des = c.findall("destructors_t")
    for d in des:
        if access_level[d] != "private":
            return 0

    # check for a public function that returns an instance of the object
    public_funcs = [x for x in access_level if access_level[x] == "public" and x in c.findall(".//member_function_t")]
    func_count = 0
    for x in public_funcs:
        return_type = x.find("return_type")
        is_static = x.find("is_static")
        if return_type.attrib['value'].find(c.attrib['value']) != 1 and is_static.attrib['value'] == "1":
            func_count += 1
    if func_count == 0:
        return 0
    if count > 1:
        return 2
    else:
        return 1


def is_strategy_pattern(root, parent_map):
    ns_tag = root.find("namespace_t").attrib['value']
    classes = root.findall(".//class_t")
    class_tags = [x.attrib['value'] for x in classes]
    for c in classes:
        vars = c.findall(".//variable_t")
        for var in vars:
            var_type = var.find('type').attrib['value']
            if var_type.find(ns_tag) != -1:
                var_class = classes[class_tags.index(var_type[len(ns_tag):].split()[0])]
                # Check if the interface class doesn't have the strategy choosing function
                if is_class_interface(var_class) and not is_choosing_in_interface(var_class, ns_tag):
                    return 1
    return 0


myTree = ET.parse("output_rectified.xml")
root = myTree.getroot()

parent_map = {c:p for p in root.iter() for c in p}

# Check for Singleton
classes = root.findall(".//class_t")
singleton_classes = 0

for c in classes:
    access_level = get_access_level(c)
    is_singleton_pattern = check_singleton_pattern(c, access_level)
    if is_singleton_pattern:
        if is_singleton_pattern == 1:
            print("Singleton Pattern detected")
        else:
            print("Modified Singleton Pattern detected. (Multiple instances)")
        singleton_classes += 1
if singleton_classes > 0:
    print("Total of ", str(singleton_classes), " instances of singleton classes observed.")
else:
    print("No singleton class present")

# Check for Strategy Pattern
if is_strategy_pattern(root, parent_map):
    print("Strategy Pattern detected.")
else:
    print("No Strategy Pattern detected.")
