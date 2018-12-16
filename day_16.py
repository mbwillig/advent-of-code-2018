def day_16a():
    import operator

    with open("day_16_AOC.txt") as fh:
        data = fh.readlines()

    def takedigits(instr):
        filtered = "".join([x for x in instr if (x.isdigit() | (x ==" "))])
        return [int(x) for x in filtered.split()]

    def get_all_posible_results(op,registers):
        optype1 = {  #these are easy and follew the same patters, once R[A], R[B], then R[A], B
        "add":operator.add,
        "mul":operator.mul,
        "ban":operator.and_,
        "bor":operator.or_}

        def get_i_and_r_funcs(func):
            return [lambda : func(registers[op[1]],registers[op[2]]),# b= register,
                    lambda: func(registers[op[1]], op[2])] # b= value

        filled_out_funcs = []
        for func in optype1.values():
            filled_out_funcs+=get_i_and_r_funcs(func)

        filled_out_funcs.append(lambda : op[1] ) #set
        filled_out_funcs.append(lambda : registers[op[1]])

        filled_out_funcs.append(lambda : {True:1,False:0}[op[1]>registers[op[2]]]) #greater than
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] > op[2]])
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]]>registers[op[2]]])

        filled_out_funcs.append(lambda : {True:1,False:0}[op[1]==registers[op[2]]]) # equal
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] == op[2]])
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] == registers[op[2]]])

        results = []

        for filled_out_func in filled_out_funcs:
            try:
                results.append(filled_out_func())
            except:
                results.append(float("inf"))
        return results


    inputindexes = [x for x in range(len(data)) if data[x].startswith("Before")]

    inputs = [takedigits(data[x]) for x in inputindexes]
    ops = [takedigits(data[x+1]) for x in inputindexes]
    outputs= [takedigits(data[x+2]) for x in inputindexes]

    nr_examples_with_3_or_more_possible_ops = 0
    for input,op,output in zip(inputs,ops,outputs):
        possible_results = get_all_posible_results(op,input)
        true_result = output[op[3]]
        possible_true = sum([x==true_result for x in possible_results])
        if possible_true>2:
            nr_examples_with_3_or_more_possible_ops +=1

    print("result",nr_examples_with_3_or_more_possible_ops, "out of", len(inputs))


def day_16b():
    import operator
    from collections import defaultdict

    with open("day_16_AOC.txt") as fh:
        data = fh.readlines()

    def takedigits(instr):
        filtered = "".join([x for x in instr if (x.isdigit() | (x ==" "))])
        return [int(x) for x in filtered.split()]

    def get_all_posible_results(op,registers):
        optype1 = {
        "add":operator.add,
        "mul":operator.mul,
        "ban":operator.and_,
        "bor":operator.or_}

        def get_i_and_r_funcs(func):
            return [lambda : func(registers[op[1]],registers[op[2]]),# b= register,
                    lambda: func(registers[op[1]], op[2])] # b= value

        filled_out_funcs = []
        for func in optype1.values():
            filled_out_funcs+=get_i_and_r_funcs(func)

        filled_out_funcs.append(lambda : op[1] ) #set
        filled_out_funcs.append(lambda : registers[op[1]])

        filled_out_funcs.append(lambda : {True:1,False:0}[op[1]>registers[op[2]]]) #greater than
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] > op[2]])
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]]>registers[op[2]]])

        filled_out_funcs.append(lambda : {True:1,False:0}[op[1]==registers[op[2]]]) # equal
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] == op[2]])
        filled_out_funcs.append(lambda : {True:1,False:0}[registers[op[1]] == registers[op[2]]])


        results = []

        for filled_out_func in filled_out_funcs:
            try:
                results.append(filled_out_func())
            except:
                results.append(float("inf"))
        return results


    inputindexes = [x for x in range(len(data)) if data[x].startswith("Before")]

    inputs = [takedigits(data[x]) for x in inputindexes]
    ops = [takedigits(data[x+1]) for x in inputindexes]
    outputs= [takedigits(data[x+2]) for x in inputindexes]

    opcode_to_result_index=defaultdict(lambda:set(range(16)))

    for input,op,output in zip(inputs,ops,outputs):
        opcode = op[0]
        possible_results = get_all_posible_results(op,input)
        true_result = output[op[3]]

        true_possible_indexes = [x for x in range(16) if possible_results[x] == true_result]
        opcode_to_result_index[opcode] &= set(true_possible_indexes)

    solved = {}
    for iter in range(12):
        for key,val in opcode_to_result_index.items():
            if len(val)==1:
                solved[key] = list(val)[0]
                for key2 in opcode_to_result_index:
                    opcode_to_result_index[key2]=opcode_to_result_index[key2]-val

    print(solved)

    ops =[takedigits(x) for x in data[inputindexes[-1]+3:] ]
    ops=[x for x in ops if len(x)>3]
    registers  = [0, 0, 0, 0]
    for op in ops:
        print(op)
        results=get_all_posible_results(op,registers)
        registers[op[3]] = results[solved[op[0]]]

    print(registers[0])

day_16b()