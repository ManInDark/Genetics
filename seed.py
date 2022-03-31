from copy import deepcopy, copy
from typing import List
from time import sleep

RESEARCH_TIME = 0


class AllelException(Exception):
    pass


class NoGenotypenException(Exception):
    pass


class NotResearchedException(Exception):
    pass


class IncompatibleException(Exception):
    pass


class Gen:

    def __hash__(self) -> int:
        return hash("".join(self.allele))

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "".join(self.allele)

    def __init__(self, allele: List[chr]) -> None:
        if len(allele) != 2:
            raise AllelException("Gene müssen 2 Allele haben: " + len(allele))
        allele.sort()
        if copy(allele[0]).lower() != copy(allele[1]).lower():
            raise AllelException("Allele müssen vom gleichen Typ sein: " + allele)
        self.allele: List[chr] = allele

    def getAllele(self) -> List:
        return self.allele

    def genType(self) -> chr:
        return copy(self.allele[0]).lower()

    def __lt__(self, other):
        return self.genType() < other.genType()

    def __gt__(self, other):
        return self.genType() > other.genType()

    def __eq__(self, other):
        return self.genType() == other.genType()

    def __le__(self, other):
        return self.genType() <= other.genType()

    def __ge__(self, other):
        return self.genType() >= other.genType()

    def __ne__(self, other):
        return self.genType() != other.genType()


class Seed:

    def __eq__(self, __o: object) -> bool:
        return True if __o.gene == self.gene and __o.researched == self.researched else False
        # NotImplemented if not type(__o) == Seed else

    def __hash__(self) -> int:
        return hash(str(self.gene) + str(self.researched))

    def __repr__(self) -> str:
        return f"({''.join((str(gen) for gen in self.gene))}, {str(self.researched)})"

    def __str__(self) -> str:
        return ''.join((str(gen) for gen in self.gene)) if self.researched else "Unbekannt"

    def __init__(self, gene: List[Gen], researched: bool = False) -> None:
        self.gene = gene
        self.gene.sort()
        self.researched: bool = researched

    def isResearched(self) -> bool:
        return self.researched

    def research(self):
        if not self.researched:
            sleep(RESEARCH_TIME)
        self.researched = True
        return self

    def getGenList(self, override=False) -> List[Gen]:
        if not self.isResearched() and not override:
            raise NotResearchedException(self)
        return self.gene


def mate(g1: Seed, g2: Seed) -> List[Seed]:
    def cloneAdd(s: Seed, g: Gen) -> Seed:
        new_s = deepcopy(s)
        new_s.gene.append(g)
        return new_s
    g1l = g1.getGenList(override=True)
    g2l = g2.getGenList(override=True)
    if not len(g1l) == len(g2l) and len(g1l) > 0:
        raise IncompatibleException("Genotyp")
    for i in range(len(g1l)):
        if not g1l[i].genType() == g2l[i].genType():
            raise IncompatibleException("Genotypgene")
    # All tests checked, genes valid and can be mated
    combination_gen_list = [Gen([allel1, allel2]) for allel2 in g2l[-1].getAllele() for allel1 in g1l[-1].getAllele()]
    if len(g1l) == 1:
        return [Seed([gen]) for gen in combination_gen_list]
    elif len(g1l) > 1:
        return [cloneAdd(pl, cgl) for cgl in combination_gen_list for pl in mate(Seed(g1l[0:len(g1l)-1]), Seed(g2l[0:len(g2l)-1]))]


class Seedbank:

    def __repr__(self) -> str:
        return self.seedbank.__repr__()

    def __str__(self) -> str:
        if len(self.seedbank) == 0:
            return "Keine Genotypen vorhanden"
        string = "Genotypen:"
        for i in range(len(self.seedbank)):
            string += f"\n {i} | {list(self.seedbank.keys())[i]} | {list(self.seedbank.values())[i]}"
        return string

    def __init__(self) -> None:
        self.seedbank: dict = {}

    def addSeed(self, seed: Seed):
        try:
            self.seedbank[copy(seed)] += 1
        except KeyError:
            self.seedbank[copy(seed)] = 1

    def addSeeds(self, seeds: List[Seed]):
        for seed in seeds:
            self.addSeed(seed)

    def retrieve(self, index: int) -> Seed:
        seed = list(self.seedbank.keys())[index]
        if self.seedbank[seed] >= 1:
            self.seedbank[seed] -= 1
            return copy(seed)
        else:
            raise NoGenotypenException(seed)

    def clean(self):
        temp = True
        while temp:
            for i in range(len(self.seedbank)):
                if list(self.seedbank.values())[i] <= 0:
                    self.seedbank.pop(list(self.seedbank.keys())[i])
                    break
                if i == len(self.seedbank) - 1:
                    temp = False

    def sum(self) -> int:
        return sum(list(self.seedbank.values())[0:len(self.seedbank)])


if __name__ == "__main__":

    sb = Seedbank()
    case = 1
    if case == 0:
        sb.addSeed(Seed([Gen(['a', 'a'])]))
        sb.addSeed(Seed([Gen(['A', 'A'])]))
    elif case == 1:
        sb.addSeed(Seed([Gen(['a', 'a']), Gen(['b', 'b'])]))
        sb.addSeed(Seed([Gen(['A', 'A']), Gen(['B', 'B'])]))
    elif case == 2:
        sb.addSeed(Seed([Gen(['a', 'a']), Gen(['b', 'b']), Gen(['c', 'c'])]))
        sb.addSeed(Seed([Gen(['A', 'A']), Gen(['B', 'B']), Gen(['C', 'C'])]))
    elif case == 3:
        # man müsste bloß so ~0.11 sec warten pro Genotyp um auf ne Stunde zu kommen
        sb.addSeed(Seed([Gen(['a', 'a']), Gen(['b', 'b']), Gen(['c', 'c']), Gen(
            ['d', 'd']), Gen(['e', 'e']), Gen(['f', 'f']), Gen(['g', 'g'])]))
        sb.addSeed(Seed([Gen(['A', 'A']), Gen(['B', 'B']), Gen(['C', 'C']), Gen(
            ['D', 'D']), Gen(['E', 'E']), Gen(['F', 'F']), Gen(['G', 'G'])]))

    sb.addSeeds([se.research() for se in mate(sb.retrieve(0), sb.retrieve(1))])
    sb.clean()
    print(sb)
    sb.addSeeds([se.research() for se in mate(sb.retrieve(0), sb.retrieve(0))])
    sb.clean()
    print(sb.sum())
