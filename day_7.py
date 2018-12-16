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


