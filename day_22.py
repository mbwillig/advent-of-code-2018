import numpy as np

def day22a():
    depth = 4848
    target = [15,700] #x, y

    field_size=[x+1 for x in target][::-1]

    erosion_level = np.zeros(field_size)
    erosion_level[0,:] = ((np.array(range(field_size[1])) * 16807) + depth) % 20183
    erosion_level[:,0] = ((np.array(range(field_size[0])) * 48271) + depth) % 20183

    for rimnr in range(1,max(field_size)):

        if rimnr<field_size[1]:
            for x in range(rimnr,field_size[0]):
                erosion_level[x,rimnr] = ((erosion_level[x-1,rimnr] * erosion_level[x,rimnr-1]) +depth) % 20183

        if rimnr<field_size[0]:
            for y in range(rimnr,field_size[1]):
                erosion_level[rimnr, y] = ((erosion_level[rimnr - 1, y] * erosion_level[rimnr, y-1]) + depth) % 20183

    erosion_level[target[1],target[0]] = 0
    print(erosion_level%3)
    risk = (erosion_level%3).sum()
    print(risk)


def day22b():
    """
    Uses a height * width * n_tools matrix to represent all states and uses a heap + dijkstra to find the shortest path
    """
    from collections import defaultdict
    import heapq
    depth = 4848
    target = [15, 700]  # x, y
    field_size = [x + 100 for x in target][::-1]
    erosion_level = np.zeros(field_size)
    erosion_level[0, :] = ((np.array(range(field_size[1])) * 16807) + depth) % 20183
    erosion_level[:, 0] = ((np.array(range(field_size[0])) * 48271) + depth) % 20183

    for rimnr in range(1, max(field_size)):

        if rimnr < field_size[1]:
            for x in range(rimnr, field_size[0]):
                erosion_level[x, rimnr] = ((erosion_level[x - 1, rimnr] * erosion_level[
                    x, rimnr - 1]) + depth) % 20183

        if rimnr < field_size[0]:
            for y in range(rimnr, field_size[1]):
                erosion_level[rimnr, y] = ((erosion_level[rimnr - 1, y] * erosion_level[
                    rimnr, y - 1]) + depth) % 20183

    erosion_level[target[1], target[0]] = 0
    rock_type = erosion_level%3


    distance_matrix=np.full((field_size[0],field_size[1],3),float("inf")) #row, col, toolset (0 = neither, 1 = torch,2 = climbing
    distance_matrix[0,0,1]=0
    target_cell = [target[1], target[0],1]
    outer_limits= field_size+[3]
    vertix_distance_dict = defaultdict(lambda: float("inf"))
    vertix_heap = []


    def get_ajacent(coord):
        newcoords =[]
        for dim in range(3):
            for dir in [-1,1]:
                newcoord = list(coord[::])
                newcoord[dim]+=dir
                newcoord[2] = newcoord[2]%3 # assures you get both other options for the tool
                if (newcoord[dim] < outer_limits[dim]) and (newcoord[dim] >-1):
                    newcoords.append(tuple(newcoord))
        return newcoords

    def get_dist(coordsa,coordsb):
        if coordsb[2] == rock_type[tuple(coordsb[0:2])]: # try to combine tool and place which is not compatible
            return float("inf")
        elif coordsa[2] != coordsb[2]:
            return 7 # tool switch
        else:
            return 1 #spatial step

    def insert_new_vertixes(coords):
        ajacent_cells = get_ajacent(coords)
        unexplored_ajacent = [ajacent for ajacent in ajacent_cells if distance_matrix[tuple(ajacent)]]
        for ajacent in unexplored_ajacent:
            total_dist = get_dist(coords,ajacent) + distance_matrix[tuple(coords)]
            if total_dist<vertix_distance_dict[ajacent]: #avoid pushing useless vertixes on the heap
                vertix_distance_dict[ajacent] = total_dist
                heapq.heappush(vertix_heap,(total_dist,ajacent))

    insert_new_vertixes((0,0,1))
    while distance_matrix[tuple(target_cell)] == float("inf"):
        dist,next_vetrtix = heapq.heappop(vertix_heap) #(dist,coords)
        distance_matrix[tuple(next_vetrtix)] = dist
        insert_new_vertixes(next_vetrtix)

    print(distance_matrix[tuple(target_cell)])

day22b()

