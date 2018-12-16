def day15a():
    import copy
    INITHP = 200
    ATT = 3
    LEFT = (0,-1) #drow, dcol
    RIGHT = (0,1)
    UP =  (-1,0)
    DOWN = (1,0)
    directions = [UP,LEFT,RIGHT,DOWN]

    def make_grid():
        with open("day_15_AOC.txt") as fh:
            data = fh.readlines()

        grid = [(["#"]+list(x)+["#"]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
        grid = [["#"]*len(grid[0])]+grid + [["#"]*len(grid[0])]# pad by 1 above and below
        return grid

    grid = make_grid()
    goblindict = {}
    elfdict= {}

    heightrange = range(1,len(grid)-1)
    widthrannge = range(1,len(grid[0])-1)

    class fighter():
        def __init__(self, row, col, allies, enemies):
            self.unmoved=True
            self.row = row
            self.col = col
            self.enemies = enemies
            self.hp = INITHP
            self.allies=allies

        def attack_if_possible(self):
            minhp = float("inf")
            enemy = False
            bestloc = False


            for drow, dcol in directions:
                ajacent = (self.row + drow, self.col + dcol)
                if ajacent in self.enemies:
                    hp = self.enemies[ajacent].hp
                    if hp<minhp:
                        enemy = self.enemies[ajacent]
                        minhp = hp
                        bestloc=ajacent

            if enemy:
                enemy.hp -= ATT
                if enemy.hp <1:
                    del self.enemies[bestloc]
                return True
            return False

        def find_next_move(self):
            distance_from_self  = make_distance_dict(self.row,self.col)
            all_ajacent_to_enemies=set([])
            for enemy in self.enemies.values():
                all_ajacent_to_enemies|=set([(enemy.row+dir[0],enemy.col+dir[1]) for dir in directions])
            all_ajacent_valid_spots = set([loc for loc in all_ajacent_to_enemies if is_empty_spot(loc)])

            target_field = False
            mindist = float("inf")
            for rownr in heightrange:
                for colnr in widthrannge:
                    if ((rownr,colnr) in distance_from_self) and ((rownr,colnr) in all_ajacent_valid_spots):
                        score = distance_from_self[(rownr,colnr)]
                        if score < mindist:
                            mindist = score
                            target_field = (rownr,colnr)

            if not target_field:
                return False

            distance_from_target = make_distance_dict(*target_field)

            mindist = float("inf")
            moveloc=False
            for dir in directions:
                ajacent_to_self = (self.row+dir[0],self.col+dir[1])
                if ajacent_to_self in distance_from_target:
                    if distance_from_target[ajacent_to_self] < mindist:
                        mindist = distance_from_target[ajacent_to_self]
                        moveloc = ajacent_to_self

            return moveloc

        def move(self,loc):
            oldloc=(self.row,self.col)
            self.row=loc[0]
            self.col=loc[1]
            self.allies[loc]=self
            del self.allies[oldloc]

        def do_turn(self):
            if self.unmoved:
                self.unmoved=False
                if self.attack_if_possible():
                    return
                moveloc = self.find_next_move()
                if moveloc:
                    self.move(moveloc)
                    self.attack_if_possible()


    def is_empty_spot(loc):
        return (loc not in goblindict) and (loc not in elfdict) and (grid[loc[0]][loc[1]] == ".")

    def make_distance_dict(row,col):
        done = set([(row,col)])
        next = [(row,col)]

        dist = 0
        distdict={}
        while next:
            next_next = []
            for loc in next:
                distdict[loc] = dist
                for ajacent in [(loc[0]+dir[0], loc[1]+dir[1]) for dir in directions]:
                    if (is_empty_spot(ajacent) and (ajacent not in done)):
                        next_next.append(ajacent)
                        done.add(ajacent)
            dist+=1
            next = next_next
        #print_distance_map(distdict)
        return distdict


    for rownr in heightrange:
        for colnr in widthrannge:
            if grid[rownr][colnr]=="G":
                goblindict[(rownr,colnr)]= (fighter(rownr,colnr,goblindict,elfdict))
                grid[rownr][colnr] = "."
            if grid[rownr][colnr]=="E":
                elfdict[(rownr,colnr)] = (fighter(rownr,colnr,elfdict,goblindict))
                grid[rownr][colnr] = "."

    def print_grid():
        gridcopy =copy.deepcopy(grid)
        for rownr,colnr in elfdict:
            gridcopy[rownr][colnr]="E"
        for rownr,colnr in goblindict:
            gridcopy[rownr][colnr]="G"
        for row in gridcopy[1:-1]:
            print("".join(row[1:-2]).rstrip())

        for rownr in heightrange:
            for colnr in widthrannge:
                for x in [goblindict,elfdict]:
                    if (rownr,colnr) in x:
                        print(x[(rownr,colnr)].hp)

        print("")

    def print_distance_map(distance_dict):
        gridcopy = copy.deepcopy(grid)
        for rownr, colnr in distance_dict:
            gridcopy[rownr][colnr] = str(distance_dict[(rownr,colnr)])
        for row in gridcopy[1:-1]:
            print("".join(row[1:-2]).rstrip())
        print("")



    def simulate_combat():
        for turn in range(200):
            for character in (list(elfdict.values()) + list(goblindict.values())):
                character.unmoved = True
            #print_grid()
            for rownr in heightrange:
                for colnr in widthrannge:
                    if (rownr,colnr) in elfdict:
                        if len(goblindict) == 0:
                            return (turn ) * sum([elf.hp for elf in elfdict.values()])
                        elfdict[(rownr,colnr)].do_turn()
                    if (rownr,colnr) in goblindict:
                        if len(elfdict) < 1:
                            return (turn) * sum([goblin.hp for goblin in goblindict.values()])
                        goblindict[(rownr,colnr)].do_turn()


    print(simulate_combat())


def day15b():

    def run_with_one_attack_power(att_elf):
        import copy
        INITHP = 200
        ATT_GOBLIN = 3
        LEFT = (0,-1) #drow, dcol
        RIGHT = (0,1)
        UP =  (-1,0)
        DOWN = (1,0)
        directions = [UP,LEFT,RIGHT,DOWN]



        def make_grid():
            with open("day_15_AOC.txt") as fh:
                data = fh.readlines()

            grid = [(["#"]+list(x)+["#"]) for x in data] # split into list and pad by 1 to the sides to avoid misindexing
            grid = [["#"]*len(grid[0])]+grid + [["#"]*len(grid[0])]# pad by 1 above and below
            return grid

        grid = make_grid()
        goblindict = {}
        elfdict= {}

        heightrange = range(1,len(grid)-1)
        widthrannge = range(1,len(grid[0])-1)

        class fighter():
            def __init__(self, row, col, allies, enemies,att):
                self.unmoved=True
                self.row = row
                self.col = col
                self.enemies = enemies
                self.hp = INITHP
                self.allies=allies
                self.att = att

            def attack_if_possible(self):
                minhp = float("inf")
                enemy = False
                bestloc = False


                for drow, dcol in directions:
                    ajacent = (self.row + drow, self.col + dcol)
                    if ajacent in self.enemies:
                        hp = self.enemies[ajacent].hp
                        if hp<minhp:
                            enemy = self.enemies[ajacent]
                            minhp = hp
                            bestloc=ajacent

                if enemy:
                    enemy.hp -= self.att
                    if enemy.hp <1:
                        del self.enemies[bestloc]
                    return True
                return False

            def find_next_move(self):
                distance_from_self  = make_distance_dict(self.row,self.col)
                all_ajacent_to_enemies=set([])
                for enemy in self.enemies.values():
                    all_ajacent_to_enemies|=set([(enemy.row+dir[0],enemy.col+dir[1]) for dir in directions])
                all_ajacent_valid_spots = set([loc for loc in all_ajacent_to_enemies if is_empty_spot(loc)])

                target_field = False
                mindist = float("inf")
                for rownr in heightrange:
                    for colnr in widthrannge:
                        if ((rownr,colnr) in distance_from_self) and ((rownr,colnr) in all_ajacent_valid_spots):
                            score = distance_from_self[(rownr,colnr)]
                            if score < mindist:
                                mindist = score
                                target_field = (rownr,colnr)

                if not target_field:
                    return False

                distance_from_target = make_distance_dict(*target_field)

                mindist = float("inf")
                moveloc=False
                for dir in directions:
                    ajacent_to_self = (self.row+dir[0],self.col+dir[1])
                    if ajacent_to_self in distance_from_target:
                        if distance_from_target[ajacent_to_self] < mindist:
                            mindist = distance_from_target[ajacent_to_self]
                            moveloc = ajacent_to_self

                return moveloc

            def move(self,loc):
                oldloc=(self.row,self.col)
                self.row=loc[0]
                self.col=loc[1]
                self.allies[loc]=self
                del self.allies[oldloc]

            def do_turn(self):
                if self.unmoved:
                    self.unmoved=False
                    if self.attack_if_possible():
                        return
                    moveloc = self.find_next_move()
                    if moveloc:
                        self.move(moveloc)
                        self.attack_if_possible()


        def is_empty_spot(loc):
            return (loc not in goblindict) and (loc not in elfdict) and (grid[loc[0]][loc[1]] == ".")

        def make_distance_dict(row,col):
            done = set([(row,col)])
            next = [(row,col)]

            dist = 0
            distdict={}
            while next:
                next_next = []
                for loc in next:
                    distdict[loc] = dist
                    for ajacent in [(loc[0]+dir[0], loc[1]+dir[1]) for dir in directions]:
                        if (is_empty_spot(ajacent) and (ajacent not in done)):
                            next_next.append(ajacent)
                            done.add(ajacent)
                dist+=1
                next = next_next
            #print_distance_map(distdict)
            return distdict


        for rownr in heightrange:
            for colnr in widthrannge:
                if grid[rownr][colnr]=="G":
                    goblindict[(rownr,colnr)]= (fighter(rownr,colnr,goblindict,elfdict,ATT_GOBLIN))
                    grid[rownr][colnr] = "."
                if grid[rownr][colnr]=="E":
                    elfdict[(rownr,colnr)] = (fighter(rownr,colnr,elfdict,goblindict,att_elf))
                    grid[rownr][colnr] = "."

        def print_grid():
            gridcopy =copy.deepcopy(grid)
            for rownr,colnr in elfdict:
                gridcopy[rownr][colnr]="E"
            for rownr,colnr in goblindict:
                gridcopy[rownr][colnr]="G"
            for row in gridcopy[1:-1]:
                print("".join(row[1:-2]).rstrip())

            for rownr in heightrange:
                for colnr in widthrannge:
                    for x in [goblindict,elfdict]:
                        if (rownr,colnr) in x:
                            print(x[(rownr,colnr)].hp)

            print("")

        def print_distance_map(distance_dict):
            gridcopy = copy.deepcopy(grid)
            for rownr, colnr in distance_dict:
                gridcopy[rownr][colnr] = str(distance_dict[(rownr,colnr)])
            for row in gridcopy[1:-1]:
                print("".join(row[1:-2]).rstrip())
            print("")



        def simulate_combat():
            inital_number_of_elves = len(elfdict)
            for turn in range(200):
                for character in (list(elfdict.values()) + list(goblindict.values())):
                    character.unmoved = True
                #print_grid()
                for rownr in heightrange:
                    for colnr in widthrannge:
                        if (rownr,colnr) in elfdict:
                            if len(goblindict) == 0:
                                return (turn ) * sum([elf.hp for elf in elfdict.values()])
                            elfdict[(rownr,colnr)].do_turn()
                        if (rownr,colnr) in goblindict:
                            if len(elfdict) < inital_number_of_elves :
                                return False
                            goblindict[(rownr,colnr)].do_turn()

        return(simulate_combat())

    for att in range(1,100):
        score = run_with_one_attack_power(att)
        if score:
            return score



