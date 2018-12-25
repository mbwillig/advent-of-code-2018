def day25a():
    from collections import defaultdict
    with open("day_25_AOC.txt") as fh:
        data = [x.strip() for x in fh.readlines()]

    def takedigits(instr):
        filtered = "".join([x if (x.isdigit() | (x == "-")) else " " for x in instr])
        return tuple([int(x) for x in filtered.split()])

    def dist(a,b):
        return sum([abs(c-d) for c,d in zip(a,b)])

    pointcoords = [takedigits(x) for x in data]

    connectdist=defaultdict(list)

    # brute force, for greater number of stares, check for surrounding of each stars for O(n) instead of O(n^2) time
    for pointnr_a in range(len(pointcoords)):
        for pointnr_b in range(pointnr_a+1,len(pointcoords)):
            point_a = pointcoords[pointnr_a]
            point_b = pointcoords[pointnr_b]
            if dist(point_a,point_b) < 4:
                connectdist[point_a].append(point_b)
                connectdist[point_b].append(point_a)

    not_done = set(pointcoords)
    groups = 0
    while not_done:
        nodes = set([not_done.pop()])
        while nodes:
            new_nodes=set([])
            for node in nodes:
                for connected_node in connectdist[node]:
                    if connected_node in not_done:
                        new_nodes.add(connected_node)
                        not_done.remove(connected_node)
            nodes = new_nodes
        groups+=1

    print(groups)

day25a()

