def day20():
    import copy
    with open("day_20_AOC.txt") as fh:
        data = fh.read().strip()

    from collections import defaultdict
    connectionsdict= defaultdict(set)

    dir_dict = {"E":1,"W":-1,"N":-1j,"S":1j}

    positions = set([0])
    stack = []

    for symbol in data:
        if symbol in dir_dict:
            for pos in positions:
                connectionsdict[pos].add(pos+dir_dict[symbol])
                connectionsdict[pos + dir_dict[symbol]].add(pos)

            positions =[pos + dir_dict[symbol] for pos in positions]

        elif symbol == '(':
            stack.append(copy.deepcopy(positions))

        elif symbol == '|':
            positions = copy.deepcopy(stack[-1])

        elif symbol == ')':
            positions = stack.pop()

    def walk_connectiondict():
        dist=-1
        distdict={0:0}
        points = set([0])
        done = set([0])
        while points:
            newpoints=set([])
            dist+=1
            for point in points:
                distdict[point] = dist
                for connection in connectionsdict[point]:
                    if connection not in done:
                        newpoints.add(connection)
                        done.add(connection)
            points=newpoints
        return distdict

    distdict = walk_connectiondict()

    print(max(distdict.values()))
    print(sum([val >= 1000 for val in distdict.values()]))

day20()



