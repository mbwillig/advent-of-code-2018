def day1a():
    with open("input_1_AOC_2018") as fh:
        data = fh.readlines()
        print(sum([float(x.strip()) for x in data]))


def day1b():
    from itertools import cycle

    with open("input_1_AOC_2018") as fh:
        data = fh.readlines()

    done = set([0])
    cumsum = 0
    for x in cycle(data):
        cumsum += int(x.strip())
        if cumsum in done:
            print(cumsum)
            break
        done.add(cumsum)

