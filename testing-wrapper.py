import unittest
from seed import Seed, Gen
from wrapper import parseInput, seedbank, reload


class Testing(unittest.TestCase):

    def setUp(self) -> None:
        reload()

    def test_clean(self):
        parseInput("r 0")
        self.assertEqual(parseInput("c"), "Erfolgreich")
        self.assertEqual(len(seedbank.seedbank), 2)
        self.assertEqual(seedbank.retrieve(1), Seed([Gen(['a', 'a'])], researched=True))

    def test_help(self):
        self.assertEqual(parseInput('h'), "clean, exit, help, list, mate, research")

    def test_list(self):
        self.assertEqual(parseInput('l'), seedbank)

    def test_research(self):
        self.assertEqual(parseInput("r 0"), "Erfolgreich")
        self.assertEqual(parseInput("r 1"), "Erfolgreich")
        self.assertEqual(seedbank.retrieve(2), Seed([Gen(['a', 'a'])], researched=True))
        self.assertEqual(seedbank.retrieve(3), Seed([Gen(['A', 'A'])], researched=True))

    def test_research_all(self):
        self.assertEqual(parseInput("ra"), "Erfolgreich")
        self.assertEqual(seedbank.retrieve(2), Seed([Gen(['a', 'a'])], researched=True))
        self.assertEqual(seedbank.retrieve(3), Seed([Gen(['A', 'A'])], researched=True))

    def test_mate(self):
        parseInput("r 0")
        parseInput("r 1")
        self.assertEqual(parseInput("m 2 3"), "Erfolgreich")
        self.assertEqual(seedbank.sum(), 4)
        self.assertEqual(seedbank.retrieve(4), Seed([Gen(['A', 'a'])]))

    def test_nichts(self):
        self.assertEqual(parseInput(" "), "Nichts")

    def test_valider_input(self):
        self.assertEqual(parseInput("r e"), "Fehlerhafte Eingabe")


if __name__ == "__main__":
    unittest.main()
