def day23a():
    with open("day_23_AOC.txt") as fh:
        data = [x.strip() for x in fh.readlines()]

    def takedigits(instr):
        filtered = "".join([x if (x.isdigit() | (x == "-")) else " " for x in instr])
        return [int(x) for x in filtered.split()]

    def get_dist(a,b):
        return sum([abs(a[x]-b[x]) for x in range(3)])

    nanobots = [takedigits(x) for x in data]
    nanobots = sorted(nanobots,key= lambda x: x[3])

    largest_range_nanobot = nanobots[-1]

    in_range_count=0
    for nanobot in nanobots:
        if get_dist(nanobot,largest_range_nanobot) <= largest_range_nanobot[-1]:
            in_range_count+=1

    print(in_range_count,"out of", len(nanobots))

def day23b():
    """ inspired by https://github.com/msullivan/advent-of-code/blob/master/2018/23b.py"""
    with open("day_23_AOC.txt") as fh:
        data = [x.strip() for x in fh.readlines()]

    def takedigits(instr):
        filtered = "".join([x if (x.isdigit() | (x == "-")) else " " for x in instr])
        return [int(x) for x in filtered.split()]

    nanobots = [takedigits(x) for x in data]

    from z3 import *
    total_in_range = Int("total_in_range")
    x = Int("x")
    y = Int("y")
    z = Int("z")

    def z_abs(a):
        return If(a >= 0, a, -a)

    def in_range(botx, boty, botz, botrange):
        return If((z_abs(botx - x) + z_abs(boty - y) + z_abs(botz - z)) > botrange, 0, 1)

    o = Optimize()

    total_in_range = sum([in_range(*bot) for bot in nanobots])

    o.maximize(total_in_range)
    o.minimize(sum([z_abs(dim - 0) for dim in [x, y, z]]))

    print(o.check())
    print(o.model())
    print(sum([abs(o.model()[val].as_long()) for val in [x, y, z]]))
