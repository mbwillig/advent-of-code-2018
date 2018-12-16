def day10():
    from collections import defaultdict

    with open("day_10_AOC.txt") as fh:
        data = fh.readlines()

    positiondict = defaultdict(list)
    for line in data:
        line = "".join([x for x in line if (x.isdigit() | (x in set(" -")))])
        x, y, dx, dy = [int(x) for x in line.split()]
        positiondict[(x, y)].append((dx, dy))

    def calc_cohesion(positiondict, linedist=1):  # based on lines of connecting points
        total = 0
        for x, y in positiondict:
            for sign in [-1, 1]:
                if all([(x + sign * dist, y) in positiondict for dist in range(1, linedist + 1)]):
                    total += 1
                if all([(x, y + sign * dist) in positiondict for dist in range(1, linedist + 1)]):
                    total += 1

        return total

    def move_one_sec(positiondict):
        new_dict = defaultdict(list)

        for x, y in positiondict:
            for dx, dy in positiondict[(x, y)]:
                new_dict[x + dx, y + dy].append((dx, dy))

        return new_dict

    bestsecond = -1
    bestscore = -1
    bestpositions = {}
    for second in range(50000):
        score = calc_cohesion(positiondict, 2)
        if score > bestscore:
            bestscore = score
            bestsecond = second
            bestpositions = positiondict
        # print(bestscore)
        positiondict = move_one_sec(positiondict)

    def print_stars(positiondict):
        xcoords, ycoords = [[x[y] for x in positiondict.keys()] for y in [0, 1]]
        minx, miny = [min(x) for x in [xcoords, ycoords]]
        maxx, maxy = [max(x) for x in [xcoords, ycoords]]
        for row in range(miny, maxy + 1):
            print("".join(["#" if (col, row) in positiondict else " " for col in range(minx, maxx + 1)]), "\n")

    print_stars(bestpositions)

    print(bestscore)
    print(bestsecond)
    print_stars(bestpositions)


