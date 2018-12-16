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