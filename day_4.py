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


