def day17():
    from collections import deque
    def takedigits(instr):
        starts_with_x = instr[0]=="x"
        filtered = "".join([x if x.isdigit() else " "  for x in instr])
        return [starts_with_x]+[int(x) for x in filtered.split()]

    with open("day_17_AOC.txt") as fh:
        data = [takedigits(x) for x in fh.readlines()]

    clayset = set([])
    for line in data:
        if line[0]:
            x, y0, y1 = line[1:]
            for y in range(y0,y1+1):
                clayset.add((x,y))
        else:
            y, x0, x1 = line[1:]
            for x in range(x0,x1+1):
                clayset.add((x,y))

    waterset=set([])
    flowing_water_set=set([])

    start_points =set([(500,0)])
    registered_points = set([(500,0)])

    minx = min([x[0] for x in clayset])
    maxx = max([x[0] for x in clayset])
    miny = min([x[1] for x in clayset])
    maxy = max([x[1] for x in clayset])

    columns_of_interest = set(range(minx-1,maxx+2))


    def hflow_one_side(current_row, current_col,d_col=1): # dcol = 1 when searching right and -1 left
        while True:
            cell_below = (current_col, current_row + 1)
            cell_ajacent = (current_col+d_col, current_row)
            if (cell_below not in waterset) and (cell_below not in clayset):
                return ["hole",cell_below]
            if (cell_ajacent in clayset):
                return ["wall",(current_col,current_row)] #return cell ajacent to wall, last cell to hold water)
            current_col+=d_col


    def do_hflow(current_row, current_col):
        sideflow_results= [hflow_one_side(current_row, current_col,d_col=x) for x in [-1,1]]
        hole_locs = [x[1] for x in sideflow_results if x[0] == "hole"]
        if len(hole_locs) ==2:
            if hole_locs[1] not in registered_points:
                registered_points.add(hole_locs[1])
                start_points.add(hole_locs[1])
                flowing_water_set.update([(col, current_row) for col in range(hole_locs[0][0],hole_locs[1][0]+1)])
                return(["hole",hole_locs[0]])
            else:
                hole_locs=hole_locs[:-1]
        if len(hole_locs)==1:
            flowing_water_set.update([(col, current_row) for col in range(sideflow_results[0][1][0],
                                                                          sideflow_results[1][1][0]+1)])
            return ["hole",hole_locs[0]] #return hole if one side has one

        return ["walls",[x[1][0] for x in sideflow_results]] #return column nrs for walls


    while start_points:
        #start one cascade
        start_loc = start_points.pop()
        current_col,current_row = start_loc
        water_vertical_flow_record=deque([(current_col, current_row)])

        while current_row<= maxy:
            cell_below = (current_col,current_row+1)
            if (cell_below in waterset) or (cell_below in clayset):
                walls_or_hole, locationdata = do_hflow(current_row,current_col)

                if walls_or_hole == "hole":
                    water_vertical_flow_record.append((current_col, current_row))
                    current_col,current_row = locationdata

                elif walls_or_hole == "walls":
                    waterfields = [(col,current_row) for col in range(locationdata[0],locationdata[1]+1)]
                    waterset.update(waterfields)

                    return_loc = water_vertical_flow_record.pop()
                    if return_loc == start_loc:
                        break
                    else:
                        current_col, current_row = return_loc

            else: #we can drop down
                water_vertical_flow_record.append((current_col, current_row))
                flowing_water_set.add((current_col, current_row))
                current_col,current_row = cell_below

        def print_grid():
            for rownr in range(miny,maxy+1):
                row=[]
                for colnr in range(minx,maxx+1):
                    symbol = '.'
                    if (colnr,rownr) in clayset:
                        symbol = "#"
                    if (colnr,rownr) in flowing_water_set:
                        symbol = "|"
                    if (colnr,rownr) in waterset:
                        symbol ="~"
                    row.append(symbol)
                print("".join(row))


    print_grid()
    all_water = waterset|flowing_water_set
    print("nr of water",len([(x,y) for x,y in all_water if (y<= maxy) and (y>= miny)]))
    print("nr of stored water",len([(x, y) for x, y in waterset if (y <= maxy) and (y >= miny)]))
day17()

