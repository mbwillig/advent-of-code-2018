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


