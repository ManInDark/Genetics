from seed import Gen, IncompatibleException, NoGenotypenException, NotResearchedException, Seed, Seedbank, mate

seedbank = Seedbank()


def reload():
    seedbank.seedbank.clear()
    seedbank.addSeed(Seed([Gen(['a', 'a'])]))
    seedbank.addSeed(Seed([Gen(['A', 'A'])]))


def parseInput(inp: str):
    inp = inp.strip()
    spl = inp.split(" ")
    try:
        if spl[0] in ["c", "clean"]:
            seedbank.clean()
            return "Erfolgreich"
        elif spl[0] in ["e", "exit"]:
            exit()
        elif spl[0] in ["h", "help"]:
            return "clean, exit, help, list, mate, research"
        elif spl[0] in ["l", "list"]:
            return seedbank
        elif spl[0] in ["m", "mate"]:
            if len(spl) != 3:
                return "Es müssen genau 2 Genotypen angegeben werden"
            spl[1] = int(spl[1])
            spl[2] = int(spl[2])
            seedbank.addSeeds(mate(seedbank.retrieve(spl[1]), seedbank.retrieve(spl[2])))
            return "Erfolgreich"
        elif spl[0] in ["r", "research"]:
            if len(spl) != 2:
                return "Es muss genau 1 Genotyp angegeben werden, der erforscht werden sollte"
            spl[1] = int(spl[1])
            seedbank.addSeed(seedbank.retrieve(spl[1]).research())
            return "Erfolgreich"
        elif spl[0] in ["ra"]:
            for i in range(len(seedbank.seedbank)):
                if list(seedbank.seedbank.keys())[i].isResearched():
                    continue
                while list(seedbank.seedbank.values())[i] > 0:
                    seedbank.addSeed(seedbank.retrieve(i).research())
            return "Erfolgreich"
        elif spl[0] in [" ", ""]:
            return "Nichts"
        else:
            return f"Nicht erkannt: {inp}"
    except NoGenotypenException:
        return "Nicht genügend Genotypen."
    except NotResearchedException:
        return "Ein Genotyp wurde noch nicht erforscht."
    except IncompatibleException:
        return "Diese Genotypen sind nicht kompatibel."
    except ValueError:
        return "Fehlerhafte Eingabe"


if __name__ == "__main__":
    reload()
    print("h für hilfe")
    while True:
        print(parseInput(input(" >")))
