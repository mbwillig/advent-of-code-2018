def day2a():
    from collections import Counter
    with open("day_2_AOC.txt") as fh:
        data = fh.readlines()

    doubles = 0
    tripples = 0

    for x in data:
        counts = Counter(x.strip()).values()
        if 2 in counts:
            doubles += 1
        if 3 in counts:
            tripples += 1

    print(doubles * tripples)


def day2b():
    with open("day_2_AOC.txt") as fh:
        data = fh.readlines()

    storage = []
    data = [list(x.strip()) for x in data]

    for x in data:
        for item in storage:
            check = [z != y for z, y in zip(x, item)]
            if sum(check) == 1:
                ans = ""
                for y, z in zip(x, item):
                    if y == z:
                        ans += y
                print(ans)
        storage.append(x)

