def day1a():
    with open("input_1_AOC_2018") as fh:
        data = fh.readlines()
        print(sum([float(x.strip()) for x in data]))


def day1b():
    from itertools import cycle

    with open("input_1_AOC_2018") as fh:
        data = fh.readlines()

    maxiter = 10 ** 8
    done = set([0])
    cumsum = 0
    for x in cycle(data):
        cumsum += int(x.strip())
        if cumsum in done:
            print(cumsum)
            break
        done.add(cumsum)

    print(len(list(done)))


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


def day3a():
    import numpy as np

    cloth = np.zeros([1000, 1000])

    with open("day_3_AOC") as fh:
        data = fh.readlines()

    for request in data:
        requestnr, _, offsets, size = request.strip().split(" ")
        requestnr = int(requestnr.strip("#"))
        left_offset, upper_offset = [int(x) for x in offsets.strip(":").split(",")]
        width, height = [int(x) for x in size.split("x")]
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1

    print(sum(sum(cloth > 1)))


def day3b():
    import numpy as np

    cloth = np.zeros([1000, 1000])

    with open("day_3_AOC") as fh:
        data = fh.readlines()

    def parse_request(request):
        requestnr, _, offsets, size = request.strip().split(" ")
        requestnr = int(requestnr.strip("#"))
        left_offset, upper_offset = [int(x) for x in offsets.strip(":").split(",")]
        width, height = [int(x) for x in size.split("x")]
        return [requestnr, left_offset, upper_offset, width, height]

    for request in data:
        requestnr, left_offset, upper_offset, width, height = parse_request(request)
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1

    for request in data:
        requestnr, left_offset, upper_offset, width, height = parse_request(request)
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1
        if sum(sum(cloth[left_offset:left_offset + width, upper_offset:upper_offset + height])) == height * width:
            print(requestnr)


def day4a():
    from collections import defaultdict, Counter
    import datetime

    timedict = {}

    with open("day_4_AOC.txt") as fh:
        data = fh.readlines()

    for line in data:
        date = line.strip().split(" ")[0][1:]
        time = line.strip().split(" ")[1][:-1]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        status = line.strip().split(" ")[2:]

        year, month, day = [int(x) for x in date.split("-")]
        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        timedict[dt] = status

    times = sorted(list(timedict.keys()))

    record = defaultdict(list)
    minute_record = defaultdict(list)
    sleeptime = 0
    lastfall = ""
    guard = ""
    for time in times:
        status = timedict[time]
        if status[-1] == "shift":
            record[guard].append(sleeptime)
            guard = status[1]
            sleeptime = 0

        elif status[0] == "falls":
            lastfall = time

        elif status[0] == "wakes":
            sleeptime += (time - lastfall).total_seconds() / 60
            minutes = range(lastfall.minute, time.minute)
            minute_record[guard].append(minutes)
        else:
            print("debug this code")

    max_sleep = 0
    maxguard = ""

    for guard, sleeplist in record.items():
        if sum(sleeplist) > max_sleep:
            max_sleep = sum(sleeplist)
            maxguard = guard

    totalminutes = []
    for minrange in minute_record[maxguard]:
        totalminutes += list(minrange)

    print(max(Counter(totalminutes).values()))
    print(maxguard)


def day4b():
    from collections import defaultdict, Counter
    import datetime

    timedict = {}

    with open("day_4_AOC.txt") as fh:
        data = fh.readlines()

    for line in data:
        date = line.strip().split(" ")[0][1:]
        time = line.strip().split(" ")[1][:-1]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        status = line.strip().split(" ")[2:]

        year, month, day = [int(x) for x in date.split("-")]
        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        timedict[dt] = status

    times = sorted(list(timedict.keys()))

    record = defaultdict(list)
    minute_record = defaultdict(list)
    sleeptime = 0
    lastfall = ""
    guard = ""
    sleeping = False
    for time in times:
        status = timedict[time]
        if status[-1] == "shift":
            record[guard].append(sleeptime)
            guard = status[1]
            sleeping = False
            sleeptime = 0
        elif status[0] == "falls":
            sleeping = True
            lastfall = time

        elif status[0] == "wakes":
            sleeptime += (time - lastfall).total_seconds() / 60
            sleeping = False
            minutes = range(lastfall.minute, time.minute)
            minute_record[guard].append(minutes)
        else:
            print()

    maxslp = 0
    maxmin = 0
    maxguard = ""
    for guard in minute_record:
        totalminutes = []
        for minrange in minute_record[guard]:
            totalminutes += list(minrange)
            counts = Counter(totalminutes)
            for minute, n in counts.items():
                if n > maxslp:
                    maxslp = n
                    maxmin = minute
                    maxguard = guard

    print(maxmin, maxguard)


def day5b():
    from collections import deque

    with open("day_5_AOC.txt") as fh:
        data = fh.read()

    def match(a, b):
        return (a != b) and (a.lower() == b.lower())

    dataoriginal = data.strip()

    letters = list(set(dataoriginal.lower()))
    minlen = float("inf")

    for letter in letters:
        data = "".join([x for x in dataoriginal if (x.lower() != letter)])

        todo = deque(list(data))
        done = deque([])

        a = todo.pop()
        while True:
            b = a
            a = todo.pop()
            if match(a, b):
                if done:
                    a = done.pop()
                elif todo:
                    a = todo.pop()
                else:
                    break

            else:
                done.append(b)
            if len(todo) < 1:
                done.append(a)
                break

        if len(list(done)) < minlen:
            minlen = len(list(done))

    print(minlen)


def day6b():
    # part a was lost due to a crash
    import numpy as np

    with open("day_6_AOC.txt") as fh:
        data = [x.strip().split(", ") for x in fh.readlines()]

    coordarray = np.array([(int(x[0]), int(x[1])) for x in data])

    hloc = coordarray[:, 0]
    vloc = coordarray[:, 1]
    nclust, dim = coordarray.shape

    minx, miny = coordarray.min(axis=0)
    maxx, maxy = coordarray.max(axis=0)

    minx, miny = [int(z - (10000 / nclust)) for z in [minx, miny]]
    maxx, maxy = [int(z + (10000 / nclust)) for z in [maxx, maxy]]

    hdist = np.abs(np.array(range(minx, maxx + 1) - hloc.reshape(nclust, 1) + np.zeros((maxy + 1 - miny, 1, 1))))
    vdist = np.abs(
        np.array(range(miny, maxy + 1)).reshape((maxy + 1 - miny, 1, 1)) - vloc.reshape(nclust, 1)) + np.zeros(
        (maxx + 1 - minx))
    totaldist = (hdist + vdist).sum(axis=1)
    print((totaldist < 10000).sum())


def day7a():
    from collections import defaultdict

    with open("day_7_AOC.txt") as fh:
        data = fh.readlines()

    def get_signles(x):
        return [y for y in x.split() if len(y) == 1]

    graph = defaultdict(lambda: {"in": [], "out": [], "done": 0})

    for line in data:
        first, second = get_signles(line)
        graph[first]["out"].append(second)
        graph[second]["in"].append(first)

    current_options = []
    for key in graph:
        if len(graph[key]["in"]) == 0:
            current_options.append(key)

    seq = []
    while current_options:
        current_options.sort()
        print(current_options)
        next_step = current_options[0]
        current_options = current_options[1:]
        seq.append(next_step)
        for dependent in graph[next_step]["out"]:
            graph[dependent]["done"] += 1
            if graph[dependent]["done"] == len(graph[dependent]["in"]):
                current_options.append(dependent)

    print("".join(seq))


def day7b():
    from collections import defaultdict
    # day 7 part 2
    with open("day_7_AOC.txt") as fh:
        data = fh.readlines()

    def get_signles(x):
        return [y for y in x.split() if len(y) == 1]

    graph = defaultdict(lambda: {"in": [], "out": [], "done": 0})

    for line in data:
        first, second = get_signles(line)
        graph[first]["out"].append(second)
        graph[second]["in"].append(first)

    current_options = []
    for key in graph:
        if len(graph[key]["in"]) == 0:
            current_options.append(key)

    class worker_instance():
        def __init__(self):
            self.task = "idle"
            self.time_task = -1
            self.last_task_ended_at = 0
            self.time_start = -1

        def is_working(self):
            return (self.task != "idle")

        def isdone(self, t):
            return self.time_task <= (t - self.time_start)

        def givetask(self, x, xt, t):
            self.time_start = t
            self.task = x
            self.time_task = xt

        def hand_over_task(self):
            task = self.task
            self.task = "idle"
            return task

    seq = []
    n_workers = 5
    t = 0
    basetime = 60
    workerlist = [worker_instance() for x in range(n_workers)]

    while len(seq) < len(graph.keys()):
        stuff_done_this_s = []
        for worker in workerlist:
            if worker.is_working():
                if worker.isdone(t):
                    stuff_done_this_s.append(worker.hand_over_task())

        for stuff in stuff_done_this_s:
            for dependent in graph[stuff]["out"]:
                graph[dependent]["done"] += 1
                if graph[dependent]["done"] == len(graph[dependent]["in"]):
                    current_options.append(dependent)
        print(t, sorted(stuff_done_this_s))
        seq += sorted(stuff_done_this_s)
        current_options.sort()
        print(current_options)
        idleworkers = [worker for worker in workerlist if not (worker.is_working())]

        n_tasks_to_be_filled = min([len(idleworkers), len(current_options)])
        for i in range(n_tasks_to_be_filled):
            xt = ord(current_options[i]) + basetime - 64
            idleworkers[i].givetask(current_options[i], xt, t)

        current_options = current_options[n_tasks_to_be_filled:]

        t += 1

    print("".join(seq))
    print(t - 1)


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


def day9():
    from collections import deque

    nplayer = 435
    last_marble_worth = 71184 * 100  # remove the *100 for part 1

    playerscores = [0] * nplayer
    player = -1

    marblecircle = deque([])

    for marblenr in range(last_marble_worth + 1):
        player = (player + 1) % nplayer
        if (marblenr % 23) == 0 and (marblenr != 0):
            playerscores[player] += marblenr
            marblecircle.rotate(7)
            playerscores[player] += marblecircle.pop()
            marblecircle.rotate(-1)
        else:
            marblecircle.rotate(-1)
            marblecircle.append(marblenr)

    print(max(playerscores))


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


def day11():
    import numpy as np

    idnr = 5791
    rack_id = (np.int_(range(1, 301)) + 10)
    grid = ((rack_id * (np.array(range(1, 301)).reshape(300, 1))) + idnr) * rack_id
    grid = np.floor((grid % 1000) / 100) - 5

    cumsum_x = np.cumsum(grid, axis=0)  # vertical cumsum
    cumsum_x = np.concatenate([np.zeros((300)).reshape(1, 300), cumsum_x], axis=0)
    best = -100
    bestcoords = -1

    possible_grid_sizes = range(1, 301)  # change to [3] for the answer to part 1

    for size in possible_grid_sizes:
        for xcoord in range(300 - (size - 1)):
            for ycoord in range(300 - (size - 1)):
                upper_cumsum = cumsum_x[ycoord + size, xcoord:xcoord + size]
                lower_cumsum = cumsum_x[ycoord, xcoord:xcoord + size]
                score = (upper_cumsum - lower_cumsum).sum()
                if score > best:
                    best = score
                    bestcoords = (xcoord + 1, ycoord + 1, size)

    print(best, bestcoords)


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

def day13a():
    from itertools import cycle
    LEFT = (0,-1) #drow, dcol
    RIGHT = (0,1)
    UP =  (-1,0)
    DOWN = (1,0)

    oposites = {UP:DOWN,
                DOWN:UP,
                LEFT:RIGHT,
                RIGHT:LEFT}

    track_to_dir = {"+": {UP,DOWN,RIGHT,LEFT},
                    "|": {UP,DOWN},
                    "-": {LEFT,RIGHT},
                    "/u": {DOWN,RIGHT},
                    "\\u" :{DOWN,LEFT},
                    "/l" :{UP,LEFT},
                    "\\l":{UP,RIGHT},
                    " ":set([]),
                    "\n": set([]),
                    "v":{UP,DOWN,RIGHT,LEFT}}

    trainsymbol_to_dir = {
        "^" : UP,
        "<" : LEFT,
        ">" : RIGHT,
        "v" : DOWN}

    with open("day_13_AOC.txt") as fh:
        data = fh.readlines()



    grid = [([" "]+list(x)+[" "]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
    grid = [[" "]*len(grid[0])]+grid + [[" "]*len(grid[0])]# pad by 1 above and below

    def classify_tract(rownr,colnr,options):
        """ used for classifying corners and pieces with a train on top"""
        for option in options:
            optionvalid = True
            for direction in track_to_dir[option]:
                ajacent_symbol = grid[rownr + direction[0]][colnr + direction[1]]
                if ajacent_symbol in {"/","\\"}:
                    optionvalid=False
                    continue
                connecting = oposites[direction] in track_to_dir[ajacent_symbol]
                if not connecting:
                    optionvalid=False
            if optionvalid:
                grid[rownr][colnr]=option


    class train():
        def __init__(self,row,col,dir):
            self.row = row
            self.col = col
            self.dir = dir
            self.crossings_taken = 0

        def updatedir(self):
            symbol = grid[self.row][self.col]

            if symbol != "+":
                newdir = [x for x in track_to_dir[symbol] if x != oposites[self.dir]][0] #cannot reverse
            else:
                clockwisedict={LEFT:UP,UP:RIGHT,RIGHT:DOWN,DOWN:LEFT}
                cyclenr = [3,0,1] #first cycle 3, then 0, then 1, never 2 as that is backwards
                dir = self.dir
                for i in range(cyclenr[self.crossings_taken%3]):

                    dir = clockwisedict[dir]
                self.crossings_taken += 1
                newdir = dir

            self.dir=newdir

        def move(self):
            self.row = self.row + self.dir[0]
            self.col = self.col + self.dir[1]

        def has_collided(self):
            collissions = [((self.row == other.row) and (self.col == other.col)) for other in trainlist ] #will collide with self
            if sum(collissions)>1:
                print("crash at",self.col-1,self.row-1,"turn",step)
                return True
            return False


    trainlist=[]

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in { "\\", "/"}:
                classify_tract(rownr, colnr,[symbol+"l",symbol+"u"])

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in trainsymbol_to_dir:
                trainlist.append(train(rownr,colnr,trainsymbol_to_dir[symbol]))
                classify_tract(rownr, colnr, ["|","-"])

    def print_grid():
        trainpositions = [(x.row, x.col) for x in trainlist]
        for rownr in range(len(grid)):
            row = []
            for colnr in range(len(grid[rownr])):
                if (rownr,colnr) in trainpositions:
                    row.append("O")
                else:
                    row.append(grid[rownr][colnr][0])
            print("".join(row).rstrip())

#    for row in grid:
#        print(row)

    for step in range(200):
        #print_grid()
        trainlist.sort(key = lambda x: x.row*1000+x.col)
        for train in trainlist:
            train.updatedir()
            train.move()
            if train.has_collided():
                print(step)
                return




def day13b():
    from itertools import cycle
    LEFT = (0,-1) #drow, dcol
    RIGHT = (0,1)
    UP =  (-1,0)
    DOWN = (1,0)

    oposites = {UP:DOWN,
                DOWN:UP,
                LEFT:RIGHT,
                RIGHT:LEFT}

    track_to_dir = {"+": {UP,DOWN,RIGHT,LEFT},
                    "|": {UP,DOWN},
                    "-": {LEFT,RIGHT},
                    "/u": {DOWN,RIGHT},
                    "\\u" :{DOWN,LEFT},
                    "/l" :{UP,LEFT},
                    "\\l":{UP,RIGHT},
                    " ":set([]),
                    "\n": set([]),
                    "v":{UP,DOWN,RIGHT,LEFT}}

    trainsymbol_to_dir = {
        "^" : UP,
        "<" : LEFT,
        ">" : RIGHT,
        "v" : DOWN}

    with open("day_13_AOC.txt") as fh:
        data = fh.readlines()



    grid = [([" "]+list(x)+[" "]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
    grid = [[" "]*len(grid[0])]+grid + [[" "]*len(grid[0])]# pad by 1 above and below

    def classify_tract(rownr,colnr,options):
        """ used for classifying corners and pieces with a train on top"""
        for option in options:
            optionvalid = True
            for direction in track_to_dir[option]:
                ajacent_symbol = grid[rownr + direction[0]][colnr + direction[1]]
                if ajacent_symbol in {"/","\\"}:
                    optionvalid=False
                    continue
                connecting = oposites[direction] in track_to_dir[ajacent_symbol]
                if not connecting:
                    optionvalid=False
            if optionvalid:
                grid[rownr][colnr]=option


    class train():
        def __init__(self,row,col,dir):
            self.row = row
            self.col = col
            self.dir = dir
            self.crossings_taken = 0
            self.colided = False

        def updatedir(self):
            symbol = grid[self.row][self.col]

            if symbol != "+":
                newdir = [x for x in track_to_dir[symbol] if x != oposites[self.dir]][0] #cannot reverse
            else:
                clockwisedict={LEFT:UP,UP:RIGHT,RIGHT:DOWN,DOWN:LEFT}
                cyclenr = [3,0,1] #first cycle 3, then 0, then 1, never 2 as that is backwards
                dir = self.dir
                for i in range(cyclenr[self.crossings_taken%3]):

                    dir = clockwisedict[dir]
                self.crossings_taken += 1
                newdir = dir

            self.dir=newdir

        def move(self):
            self.row = self.row + self.dir[0]
            self.col = self.col + self.dir[1]

        def has_collided(self):
            for other in trainlist:
                if other != self:
                    if (self.row == other.row) and (self.col == other.col):
                        self.colided=True
                        other.colided=True
                        print("crash at",self.col-1,self.row-1,"turn",step)

            return False


    trainlist=[]

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in { "\\", "/"}:
                classify_tract(rownr, colnr,[symbol+"l",symbol+"u"])

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in trainsymbol_to_dir:
                trainlist.append(train(rownr,colnr,trainsymbol_to_dir[symbol]))
                classify_tract(rownr, colnr, ["|","-"])

    def print_grid():
        trainpositions = [(x.row, x.col) for x in trainlist]
        for rownr in range(len(grid)):
            row = []
            for colnr in range(len(grid[rownr])):
                if (rownr,colnr) in trainpositions:
                    row.append("O")
                else:
                    row.append(grid[rownr][colnr][0])
            print("".join(row).rstrip())

#    for row in grid:
#        print(row)

    for step in range(20000):
        if len(trainlist) <2:
            print("train remaining at", trainlist[0].col - 1, trainlist[0].row - 1, "turn", step)
            return
        trainlist.sort(key = lambda x: x.row*1000+x.col)
        for train in trainlist:
            train.updatedir()
            train.move()
            train.has_collided()
            trainlist = list(filter(lambda x: not x.colided, trainlist))

day13b()
