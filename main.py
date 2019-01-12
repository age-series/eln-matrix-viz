#!/usr/bin/python3

# counters for subystems, nodes, and nulls
sysID = 0
maxID = 0
nullID = 0

# Node object with parser
class Node:
    global maxID, nullID

    # create the node
    def __init__(self, subsystemID):
        self.id = "" # ID for the node
        self.name = "" # Name (type) of the node
        self.ssid = subsystemID # System this node is a member of

    # parse a string which contains a Node object
    def parse(self, str):
        # Accepted language:
        # (<id> <name>)
        # null
        global maxID, nullID
        if len(str) < 1:
            return
        if str[0:1] == "(" and ")" in str:
            try:
                self.id, self.name = str[1:len(str) - 1].split(",")
            except:
                print("Invalid Node: `{}`".format(str))
        elif str[0:1] == "n":
            if str == "null":
                self.name = "null"
                self.id = "n{}".format(nullID)
                nullID = nullID + 1
            else:
                print("Invalid Node: `{}`".format(str))
        else:
            print("Invalid Node: `{}`".format(str))

# Component object with parser
class Component:

    # create the component
    def __init__(self, subsystemID):
        self.id = "" # ID for the component
        self.name = "" # Name (type) of the component
        self.ssid = subsystemID # System this component is a member of
        self.nodes = [] # list of associated nodes (two)
        self.next = None # next Component if applicable.

    # parse a string which contains Component object(s)
    def parse(self, str):
        # Accepted language:
        # [Node <name> Node]Component
        # [Node <name> Node]
        if "[" in str and "]" in str:
            now, later = str.strip()[1:].split("]",1)

            n1 = Node(self.ssid)
            n2 = Node(self.ssid)

            try:
                a, self.name, b = now.strip().split(" ")
                n1.parse(a)
                n2.parse(b)
                self.nodes.append(n1)
                self.nodes.append(n2)
            except Exception as e:
                print("Error parsing Component: `{}` for reason {}".format(now, e))

            if later.strip() != "":
                c = Component(self.ssid)
                c.parse(later.strip())
                self.next = c
        else:
            print("Invalid Component: `{}`".format(str))

# Takes in a top level component object, and creates a graphviz compatible dot graph.
def makeGraph(component):
    # If this component is nothing, let's fail now.
    if component == None:
        return ""
    c = component # component loop object
    nl = [] # node list of already created nodes
    ret = "graph subsystem{} {}".format(c.ssid, "{\n") # ret is the dot file return

    # loop for every component
    while(c != None):
        # loop for every node in component
        for node in c.nodes:
            if node.name == "null":
                # add a null node to the graph. These aren't connected to other devices,
                # so they are all unique and not possible to be duplicated.
                ret += "  {} [style=invis];\n".format(node.id)
            else:
                if not node.id in nl:
                    # add a node to the graph (if not a duplicate)
                    ret += "  {} [label={}];\n".format(node.id, node.name)
                    nl.append(node.id)
                else:
                    pass
                    #print("Node ({},{}) already in list".format(node.id, node.name))

        # add the component after the nodes
        if len(c.nodes) == 2:
            ret += "  {} -- {} [label={}];\n".format(c.nodes[0].id, c.nodes[1].id, c.name)
        else:
            # ummmmmmmmm
            print("Uhhh, error, {}".format(c.nodes))

        # step to the next object in the singly linked list.
        c = c.next

    # conclude the file format.
    return ret + "}\n"

# test node function
def testNode(str):
    n = Node(0)
    n.parse(str)
    print(n.name)
    print(n.id)

# test component function
def testComponent(str):
    c = Component(0)
    c.parse(str)
    print(c.name)

#
# MAIN
#

# read the output from Minecraft
f = open("/home/jared/.local/share/multimc/instances/testing/.minecraft/elnDumpSubSystems.txt")
lines = f.readlines()
f.close()

# create a dot file for each subsystem
for line in lines:

    # empty subsystems are dropped here
    if line.strip() == "":
        continue

    # parse from subsystem to dot format
    c = Component(sysID)
    c.parse(line)
    dotfile = makeGraph(c)

    # write out dot
    f = open("./dots/{}.dot".format(sysID), "w")
    f.write(dotfile)
    f.close()

    # last thing to do, up sysID
    sysID += 1

#
# Test Cases
#

# Test nodes
#testNode("null")
#testNode("(1,NbtElectricalLoad)")

# Test components
#testComponent("[(1,NbtElectricalLoad) Line (0,NbtElectricalLoad)]")
#testComponent("[(1,NbtElectricalGateOutput) NbtElectricalGateOutputProcess null][(0,NbtElectricalGateInput) ElectricalConnection (1,NbtElectricalGateOutput)]")

# Test making graphs from components
#c = Component(0)
#c.parse("[(1,NbtElectricalLoad) Line (0,NbtElectricalLoad)]")
#c.parse("[(1,NbtElectricalGateOutput) NbtElectricalGateOutputProcess null][(0,NbtElectricalGateInput) ElectricalConnection (1,NbtElectricalGateOutput)]")
#print(makeGraph(c))
