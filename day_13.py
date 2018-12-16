def day13a():
    from itertools import cycle
    LEFT = (0,-1) #drow, dcol
    RIGHT = (0,1)
    UP =  (-1,0)
    DOWN = (1,0)

    oposites = {UP:DOWN,
                DOWN:UP,
                LEFT:RIGHT,
                RIGHT:LEFT}

    track_to_dir = {"+": {UP,DOWN,RIGHT,LEFT},
                    "|": {UP,DOWN},
                    "-": {LEFT,RIGHT},
                    "/u": {DOWN,RIGHT},
                    "\\u" :{DOWN,LEFT},
                    "/l" :{UP,LEFT},
                    "\\l":{UP,RIGHT},
                    " ":set([]),
                    "\n": set([]),}

    trainsymbol_to_dir = {
        "^" : UP,
        "<" : LEFT,
        ">" : RIGHT,
        "v" : DOWN}

    with open("day_13_AOC.txt") as fh:
        data = fh.readlines()



    grid = [([" "]+list(x)+[" "]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
    grid = [[" "]*len(grid[0])]+grid + [[" "]*len(grid[0])]# pad by 1 above and below

    def classify_tract(rownr,colnr,options):
        """ used for classifying corners and pieces with a train on top"""
        for option in options:
            optionvalid = True
            for direction in track_to_dir[option]:
                ajacent_symbol = grid[rownr + direction[0]][colnr + direction[1]]
                if ajacent_symbol in {"/","\\"}:
                    optionvalid=False
                    continue
                connecting = oposites[direction] in track_to_dir[ajacent_symbol]
                if not connecting:
                    optionvalid=False
            if optionvalid:
                grid[rownr][colnr]=option


    class train():
        def __init__(self,row,col,dir):
            self.row = row
            self.col = col
            self.dir = dir
            self.crossings_taken = 0

        def updatedir(self):
            symbol = grid[self.row][self.col]

            if symbol != "+":
                newdir = [x for x in track_to_dir[symbol] if x != oposites[self.dir]][0] #cannot reverse
            else:
                clockwisedict={LEFT:UP,UP:RIGHT,RIGHT:DOWN,DOWN:LEFT}
                cyclenr = [3,0,1] #first cycle 3, then 0, then 1, never 2 as that is backwards
                dir = self.dir
                for i in range(cyclenr[self.crossings_taken%3]):

                    dir = clockwisedict[dir]
                self.crossings_taken += 1
                newdir = dir

            self.dir=newdir

        def move(self):
            self.row = self.row + self.dir[0]
            self.col = self.col + self.dir[1]

        def has_collided(self):
            collissions = [((self.row == other.row) and (self.col == other.col)) for other in trainlist ] #will collide with self
            if sum(collissions)>1:
                print("crash at",self.col-1,self.row-1,"turn",step)
                return True
            return False


    trainlist=[]

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in { "\\", "/"}:
                classify_tract(rownr, colnr,[symbol+"l",symbol+"u"])

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in trainsymbol_to_dir:
                trainlist.append(train(rownr,colnr,trainsymbol_to_dir[symbol]))
                classify_tract(rownr, colnr, ["|","-"])

    def print_grid():
        trainpositions = [(x.row, x.col) for x in trainlist]
        for rownr in range(len(grid)):
            row = []
            for colnr in range(len(grid[rownr])):
                if (rownr,colnr) in trainpositions:
                    row.append("O")
                else:
                    row.append(grid[rownr][colnr][0])
            print("".join(row).rstrip())

#    for row in grid:
#        print(row)

    for step in range(200):
        #print_grid()
        trainlist.sort(key = lambda x: x.row*1000+x.col)
        for train in trainlist:
            train.updatedir()
            train.move()
            if train.has_collided():
                print(step)
                return


def day13b():
    from itertools import cycle
    LEFT = (0,-1) #drow, dcol
    RIGHT = (0,1)
    UP =  (-1,0)
    DOWN = (1,0)

    oposites = {UP:DOWN,
                DOWN:UP,
                LEFT:RIGHT,
                RIGHT:LEFT}

    track_to_dir = {"+": {UP,DOWN,RIGHT,LEFT},
                    "|": {UP,DOWN},
                    "-": {LEFT,RIGHT},
                    "/u": {DOWN,RIGHT},
                    "\\u" :{DOWN,LEFT},
                    "/l" :{UP,LEFT},
                    "\\l":{UP,RIGHT},
                    " ":set([]),
                    "\n": set([])}

    trainsymbol_to_dir = {
        "^" : UP,
        "<" : LEFT,
        ">" : RIGHT,
        "v" : DOWN}

    with open("day_13_AOC.txt") as fh:
        data = fh.readlines()



    grid = [([" "]+list(x)+[" "]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
    grid = [[" "]*len(grid[0])]+grid + [[" "]*len(grid[0])]# pad by 1 above and below

    def classify_tract(rownr,colnr,options):
        """ used for classifying corners and pieces with a train on top"""
        for option in options:
            optionvalid = True
            for direction in track_to_dir[option]:
                ajacent_symbol = grid[rownr + direction[0]][colnr + direction[1]]
                if ajacent_symbol in {"/","\\"}:
                    optionvalid=False
                    continue
                connecting = oposites[direction] in track_to_dir[ajacent_symbol]
                if not connecting:
                    optionvalid=False
            if optionvalid:
                grid[rownr][colnr]=option


    class train():
        def __init__(self,row,col,dir):
            self.row = row
            self.col = col
            self.dir = dir
            self.crossings_taken = 0
            self.colided = False

        def updatedir(self):
            symbol = grid[self.row][self.col]

            if symbol != "+":
                newdir = [x for x in track_to_dir[symbol] if x != oposites[self.dir]][0] #cannot reverse
            else:
                clockwisedict={LEFT:UP,UP:RIGHT,RIGHT:DOWN,DOWN:LEFT}
                cyclenr = [3,0,1] #first cycle 3, then 0, then 1, never 2 as that is backwards
                dir = self.dir
                for i in range(cyclenr[self.crossings_taken%3]):

                    dir = clockwisedict[dir]
                self.crossings_taken += 1
                newdir = dir

            self.dir=newdir

        def move(self):
            self.row = self.row + self.dir[0]
            self.col = self.col + self.dir[1]

        def has_collided(self):
            for other in trainlist:
                if other != self:
                    if (self.row == other.row) and (self.col == other.col):
                        self.colided=True
                        other.colided=True
                        print("crash at",self.col-1,self.row-1,"turn",step)

            return False


    trainlist=[]

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in { "\\", "/"}:
                classify_tract(rownr, colnr,[symbol+"l",symbol+"u"])

    for rownr in range(len(grid)):
        for colnr in range(len(grid[rownr])):
            symbol = grid[rownr][colnr]
            if symbol in trainsymbol_to_dir:
                trainlist.append(train(rownr,colnr,trainsymbol_to_dir[symbol]))
                classify_tract(rownr, colnr, ["|","-"])

    def print_grid():
        trainpositions = [(x.row, x.col) for x in trainlist]
        for rownr in range(len(grid)):
            row = []
            for colnr in range(len(grid[rownr])):
                if (rownr,colnr) in trainpositions:
                    row.append("O")
                else:
                    row.append(grid[rownr][colnr][0])
            print("".join(row).rstrip())

#    for row in grid:
#        print(row)

    for step in range(20000):
        if len(trainlist) <2:
            print("train remaining at", trainlist[0].col - 1, trainlist[0].row - 1, "turn", step)
            return
        trainlist.sort(key = lambda x: x.row*1000+x.col)
        for train in trainlist:
            train.updatedir()
            train.move()
            train.has_collided()
            trainlist = list(filter(lambda x: not x.colided, trainlist))

