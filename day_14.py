def day14a():
    scoreboard = [3,7]
    elf_scoreboard_ix=[0,1]

    def add_new_scores():
        sum_scores = sum(scoreboard[x] for x in elf_scoreboard_ix)
        new_recepies = [int(x) for x in list(str(sum_scores))]
        scoreboard.extend(new_recepies)

    def move_elfs():
        return [(scoreboard[x]+1+x)%len(scoreboard) for x in elf_scoreboard_ix]

    puzzle_input  = 47801
    recepies_after = 10

    while len(scoreboard)<(puzzle_input+recepies_after):
        add_new_scores()
        elf_scoreboard_ix = move_elfs()

    print("".join([str(x) for x in scoreboard[puzzle_input:puzzle_input+recepies_after]]))

def day14b():
    scoreboard = [3,7]
    elf_scoreboard_ix=[0,1]

    def add_new_scores():
        sum_scores = sum(scoreboard[x] for x in elf_scoreboard_ix)
        new_recepies = [int(x) for x in list(str(sum_scores))]
        scoreboard.extend(new_recepies)

    def move_elfs():
        return [(scoreboard[x]+1+x)%len(scoreboard) for x in elf_scoreboard_ix]

    puzzle_input  ="047801"
    len_input=len(str(puzzle_input))

    while True:
        add_new_scores()
        elf_scoreboard_ix = move_elfs()
        if "".join([str(x) for x in scoreboard[-len_input:]]) == puzzle_input:
            print(len(scoreboard)-len_input)
            break
        if "".join([str(x) for x in scoreboard[(-len_input) -1:-1]]) == puzzle_input:
            print((len(scoreboard)-1) - len_input)
            break