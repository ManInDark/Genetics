from seed import Gen, IncompatibleException, NoGenotypenException, NotResearchedException, Seed, Seedbank, mate

print("h für hilfe")

seedbank = Seedbank()
seedbank.addSeed(Seed([Gen(['a', 'a'])]))
seedbank.addSeed(Seed([Gen(['A', 'A'])]))


def parseInput(inp: str):
    inp = inp.strip()
    spl = inp.split(" ")
    try:
        if spl[0] in ["c", "clean"]:
            seedbank.clean()
        elif spl[0] in ["e", "exit"]:
            exit()
        elif spl[0] in ["h", "help"]:
            print("clean, exit, help, list, mate, research")
        elif spl[0] in ["l", "list"]:
            print(seedbank)
        elif spl[0] in ["m", "mate"]:
            if len(spl) != 3:
                print("Es müssen genau 2 Genotypen angegeben werden")
                return
            spl[1] = int(spl[1])
            spl[2] = int(spl[2])
            seedbank.addSeeds(mate(seedbank.retrieve(spl[1]), seedbank.retrieve(spl[2])))
        elif spl[0] in ["r", "research"]:
            if len(spl) != 2:
                print("Es muss genau 1 Genotyp angegeben werden, der erforscht werden sollte")
                return
            spl[1] = int(spl[1])
            seedbank.addSeed(seedbank.retrieve(spl[1]).research())
        elif spl[0] in [" ", ""]:
            pass
        else:
            print(inp)
    except NoGenotypenException:
        print("Nicht genügend Genotypen.")
    except NotResearchedException:
        print("Ein Genotyp wurde noch nicht erforscht.")
    except IncompatibleException:
        print("Diese Genotypen sind nicht kompatibel.")


while True:
    parseInput(input(" >"))
