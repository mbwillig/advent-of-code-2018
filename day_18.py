def day18a():
    import numpy as np
    with open("day_18_AOC.txt") as fh:
        data = [list(x.strip()) for x in fh.readlines()]

    def count_symbol(symbol,grid):
        countgrid = -1* (grid==symbol)
        paddedgrid = np.pad(grid,((1,1),(1,1)),mode="constant")

        height, width = grid.shape
        for voff in [-1,0,1]:
            for hoff in [-1,0,1]:
                shiftedgrid = paddedgrid[1+voff:height+1+voff,1+hoff:width+1+hoff]
                countgrid += (shiftedgrid == symbol)

        return countgrid

    grid = np.array(data)
    for minute in range(10):
        treecount, opencount,lumbercount = [count_symbol(symbol,grid) for symbol in ["|",".","#"]]
        grid_copy = grid.copy()
        grid_copy[((treecount>2)*(grid==".")).astype(bool)] = "|"
        grid_copy[((lumbercount > 2) * (grid == "|")).astype(bool)] = "#"

        no_lumberyard_or_tree = np.logical_not(((lumbercount > 0) * (treecount > 0)))
        grid_copy[(no_lumberyard_or_tree * (grid== "#")).astype(bool)] = "."
        grid = grid_copy

    print((grid=="#").sum()*(grid=="|").sum())


def day18b():
    import numpy as np
    with open("day_18_AOC.txt") as fh:
        data = [list(x.strip()) for x in fh.readlines()]

    def count_symbol(symbol,grid):
        countgrid = -1* (grid==symbol)
        paddedgrid = np.pad(grid,((1,1),(1,1)),mode="constant")

        height, width = grid.shape
        for voff in [-1,0,1]:
            for hoff in [-1,0,1]:
                shiftedgrid = paddedgrid[1+voff:height+1+voff,1+hoff:width+1+hoff]
                countgrid += (shiftedgrid == symbol)

        return countgrid

    def one_minute(grid):
        treecount, opencount,lumbercount = [count_symbol(symbol,grid) for symbol in ["|",".","#"]]
        grid_copy = grid.copy()
        grid_copy[((treecount>2)*(grid==".")).astype(bool)] = "|"
        grid_copy[((lumbercount > 2) * (grid == "|")).astype(bool)] = "#"

        no_lumberyard_or_tree = np.logical_not(((lumbercount > 0) * (treecount > 0)))
        grid_copy[(no_lumberyard_or_tree * (grid== "#")).astype(bool)] = "."
        return grid_copy

    grid = np.array(data)
    total_time = 1000000000
    cycle_len = 28 #-> cycle len = 28 after some time
    for minute in range(10000):
        grid = one_minute(grid)
    for minute in range((total_time-10000)%cycle_len):
        grid = one_minute(grid)

    print((grid=="#").sum()*(grid=="|").sum())

day18b()