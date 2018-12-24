
def day24a(boost=0):
    import math
    with open("day_24_AOC.txt") as fh:
        data = [x.strip() for x in fh.readlines()]

    infectionline = [i for i in range(len((data))) if data[i].startswith("Infection")][0]

    def takedigits(instr):
        filtered = "".join([x if (x.isdigit() | (x == "-")) else " " for x in instr])
        return [int(x) for x in filtered.split()]

    def parseline(instr,boost=0):
        units,hp, dmg, init = takedigits(instr)
        att_type = instr.split("damage")[0].split()[-1]

        output ={"weak":[],
                 "immune":[],
                 "hp":hp,
                 "units":units,
                 "init":init,
                 "dmg":dmg+boost,
                 "att_type":att_type,
                 "open_for_attack":True,
                 "attacking":False}

        if "(" in instr:
            specials = instr.split("(")[1].split(")")[0].split(";")
            for special in specials:
                words = [x.strip(",") for x in special.split()]
                output[words[0]] = words[2:]

        return(output)

    def determine_dmg(a,b):
        multiplier = 1
        if a["att_type"]  in b["immune"]:
            multiplier = 0
        if a["att_type"] in b["weak"]:
            multiplier = 2

        return a["units"]*a["dmg"]*multiplier

    def target(attackkers,defenders):
        sorted_attackers = sorted(attackkers, key= lambda x : (x["units"] *x["dmg"], x["init"]),reverse=True)
        for attacker in sorted_attackers:
            sorted_defenders = sorted(defenders,key=lambda x: (x["open_for_attack"],determine_dmg(attacker,x),x["dmg"]*x["units"],x["init"]),reverse=True)

            if (sorted_defenders[0]["open_for_attack"]):
                if determine_dmg(attacker,sorted_defenders[0])>0:
                    attacker["attacking"] = sorted_defenders[0]
                    sorted_defenders[0]["open_for_attack"] = False
            else:
                break

    def do_all_attacks(units):
        dmg_done = False
        for unit in sorted(units,key = lambda x: x["init"],reverse=True):
            if unit["attacking"]:
                enemy = unit["attacking"]
                unit_dmg =  determine_dmg(unit,enemy) // enemy["hp"]
                if unit_dmg>0:
                    dmg_done = True
                enemy["units"] -=unit_dmg
                enemy["units"] = max([0,enemy["units"]])
        return dmg_done

    immune_system = []
    infection = []
    for i in range(1,infectionline-1):
        immune_system.append(parseline(data[i],boost=boost))
    for i in range(infectionline+1,len(data)):
        infection.append(parseline(data[i]))

    dmg_done = True
    while (immune_system and infection and dmg_done):
        target(immune_system,infection)
        target(infection, immune_system)
        dmg_done = do_all_attacks(infection+immune_system)
        immune_system = [x for x in immune_system if x["units"]>0]
        infection = [x for x in infection if x["units"] > 0]
        for group in (infection+immune_system):
            group["attacking"]=False
            group["open_for_attack"]=True

    if not dmg_done:
        return False

    if boost == 0:
        print("part a",sum([x["units"] for x in (immune_system+infection)]))
    return sum([x["units"] for x in (immune_system)])

def day24b():
    for boost in range(0,100):
        result = day24a(boost)
        if result:
            if result>0:
               print("part b", result)
               break
day24b()


