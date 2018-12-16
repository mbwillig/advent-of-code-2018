def day6b():
    # part a was lost due to a crash but was solved by finding the nodes that are closest to cells on the edges of the
    # grid minx - maxx, miny-maxy which have infinite areas
    import numpy as np

    with open("day_6_AOC.txt") as fh:
        data = [x.strip().split(", ") for x in fh.readlines()]

    coordarray = np.array([(int(x[0]), int(x[1])) for x in data])

    hloc = coordarray[:, 0]
    vloc = coordarray[:, 1]
    nclust, dim = coordarray.shape

    minx, miny = coordarray.min(axis=0)
    maxx, maxy = coordarray.max(axis=0)

    minx, miny = [int(z - (10000 / nclust)) for z in [minx, miny]]
    maxx, maxy = [int(z + (10000 / nclust)) for z in [maxx, maxy]]

    hdist = np.abs(np.array(range(minx, maxx + 1) - hloc.reshape(nclust, 1) + np.zeros((maxy + 1 - miny, 1, 1))))
    vdist = np.abs(
        np.array(range(miny, maxy + 1)).reshape((maxy + 1 - miny, 1, 1)) - vloc.reshape(nclust, 1)) + np.zeros(
        (maxx + 1 - minx))
    totaldist = (hdist + vdist).sum(axis=1)
    print((totaldist < 10000).sum())



