def day19a():
    import operator

    def get_all_ops():
        optype1 = {  #these are easy and follew the same patters, once R[A], R[B], then R[A], B
        "add":operator.add,
        "mul":operator.mul,
        "ban":operator.and_,
        "bor":operator.or_}

        allops ={}

        def get_i_and_r_funcs(func):
            return [lambda registers,op: func(registers[op[1]],registers[op[2]]),# b= register,
                    lambda registers,op: func(registers[op[1]], op[2])] # b= value

        filled_out_funcs = []
        for name, func in optype1.items():
            allops[name+"r"],allops[name+"i"] = get_i_and_r_funcs(func)

        allops["seti"] = lambda registers,op: op[1]  #set
        allops["setr"] = lambda registers,op: registers[op[1]]

        allops["gtir"] = lambda registers,op: {True:1,False:0}[op[1]>registers[op[2]]] #greater than
        allops["gtri"] = lambda registers,op: {True:1,False:0}[registers[op[1]] > op[2]]
        allops["gtrr"] = lambda registers,op: {True:1,False:0}[registers[op[1]]>registers[op[2]]]

        allops["eqir"] = lambda registers,op: {True:1,False:0}[op[1]==registers[op[2]]] # equal
        allops["eqri"] = lambda registers,op: {True:1,False:0}[registers[op[1]] == op[2]]
        allops["eqrr"] = lambda registers,op: {True:1,False:0}[registers[op[1]] == registers[op[2]]]

        return allops

    ops = get_all_ops()

    with open("day_19_AOC.txt") as fh:
        data = [x.strip().split() for x in fh.readlines()]

    register_ix = int(data[0][-1])
    data = data[1:]
    registers = [0]*6
    registers[0] = 1
    instructionnr=0
    while (instructionnr>-1) and instructionnr < len(data):
        instruction = data[instructionnr]
        command = instruction[0]
        A,B,C = [int(x) for x in instruction[1:]]
        registers[C] = ops[command](registers,[0,A,B,C])
        registers[register_ix] +=1
        instructionnr=registers[register_ix]
        #print(registers)

    print(registers[0])

#day19a()

def day19b():
    #completed with spoilers from reddit
    import math
    n = 10551347
    sqrtn = int(math.sqrt(n))
    totalsum=0
    for div in range(1,sqrtn+1):
        if n%div == 0:
            for devisor in set([div,n/div]):
                totalsum+= devisor

    print(totalsum)

day19b()