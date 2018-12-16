def day12():
    from collections import defaultdict

    with open("day_12_AOC.txt") as fh:
        data = fh.readlines()

    state = data[0].split(":")[1].strip()

    statedict = defaultdict(lambda: ".")

    for idx, val in enumerate(state):
        if val == "#":
            statedict[idx] = val

    instructiondict = defaultdict(lambda: ".")
    for instruction in data[2:]:
        originalstate, outputstate = [x.strip() for x in instruction.split("=>")]
        instructiondict[originalstate] = outputstate

    def print_all(statedict):
        min_plant = min([key for key, val in statedict.items() if val == "#"])
        max_plant = max([key for key, val in statedict.items() if val == "#"])
        print("".join([statedict[place] for place in range(min_plant, max_plant + 1)]))

    n_iter = 1000  # 50000000000 # after some time the score increases 55/generation

    for i in range(n_iter):
        # print_all(statedict)
        min_plant = min([key for key, val in statedict.items() if val == "#"])
        max_plant = max([key for key, val in statedict.items() if val == "#"])
        new_state = defaultdict(lambda: ".")
        for place in range(min_plant - 2, max_plant + 3):
            if instructiondict["".join([statedict[position] for position in range(place - 2, place + 3)])] == "#":
                new_state[place] = "#"
        statedict = new_state

    print(sum([key for key, val in statedict.items() if val == "#"]) + (50000000000 - 1000) * 55)

