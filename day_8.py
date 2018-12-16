def day8a():
    from collections import deque

    with open("day_8_AOC.txt") as fh:
        data = fh.read()

    dataque = deque(int(x) for x in data.split())
    dataque.reverse()

    fullgraph = {}

    def construct_node(currentnode, values):
        nchild = dataque.pop()
        nmeta = dataque.pop()
        for child in range(nchild):
            currentnode[child] = {}
            construct_node(currentnode[child], values)
        currentnode["metadata"] = []
        for metadata in range(nmeta):
            val = dataque.pop()
            values.append(val)
            currentnode["metadata"].append(val)

    values = []
    construct_node(fullgraph, values)

    print("sum of all metadat", sum(values))


def day8b():
    from collections import deque

    with open("day_8_AOC.txt") as fh:
        data = fh.read()

    dataque = deque(int(x) for x in data.split())
    dataque.reverse()

    fullgraph = {}

    def construct_node(currentnode, values):
        nchild = dataque.pop()
        nmeta = dataque.pop()
        for child in range(1, nchild + 1):
            currentnode[child] = {}
            construct_node(currentnode[child], values)
        currentnode["metadata"] = []
        for metadata in range(nmeta):
            val = dataque.pop()
            values.append(val)
            currentnode["metadata"].append(val)

    metadata = []
    construct_node(fullgraph, metadata)

    def assign_values(currentnode):
        if 1 not in currentnode:
            currentnode["value"] = sum(currentnode["metadata"])
            return

        currentnode["value"] = 0
        for metadata in currentnode["metadata"]:
            if metadata in currentnode:
                if "value" not in currentnode[metadata]:
                    assign_values(currentnode[metadata])
                currentnode["value"] += currentnode[metadata]["value"]

    assign_values(fullgraph)
    print(fullgraph["value"])


