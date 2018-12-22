def day21a():
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

    def run(data): # brute force solution that takes way too long
        reg_4_results = []
        reg_4_set=set()

        register_ix = int(data[0][-1])
        data = data[1:]
        registers = [0]*6
        instructionnr=0
        while True:
            if (instructionnr<0) or (instructionnr >= len(data)):
                return False

            if instructionnr == (len(data)-3):
                print("reg 4",registers[4])
                if registers[4] in reg_4_set:
                    return reg_4_results

                reg_4_results.append(registers[4])
                reg_4_set.add(registers[4])

            instruction = data[instructionnr]
            command = instruction[0]
            A,B,C = [int(x) for x in instruction[1:]]

            registers[C] = ops[command](registers,[0,A,B,C])

            registers[register_ix] +=1
            instructionnr=registers[register_ix]



    with open("day_21_AOC.txt") as fh:
        data = [x.strip().split() for x in fh.readlines()]


    reg_4_record = run(data=data)
    print("part a:", reg_4_record[0])
    print("part b:", reg_4_record[-1])

day21a()

