import unittest
from seed import Seedbank, Seed, Gen, mate


class Testing(unittest.TestCase):

    def setUp(self):
        self.seedbank = Seedbank()

    def test_addSeed(self):
        self.seedbank.addSeed(Seed([Gen(['a', 'a'])]))
        self.assertEqual(self.seedbank.retrieve(0), Seed([Gen(['a', 'a'])]))

    def test_addSeeds(self):
        self.seedbank.addSeeds([Seed([Gen(['A', 'A'])]), Seed([Gen(['a', 'a'])])])
        self.assertEqual(self.seedbank.retrieve(0), Seed([Gen(['A', 'A'])]))
        self.assertEqual(self.seedbank.retrieve(1), Seed([Gen(['a', 'a'])]))

    def test_retrieve(self):
        with self.assertRaises(Exception):
            self.seedbank.retrieve(0)

    def test_clean(self):
        self.seedbank.addSeed(Seed([Gen(['a', 'a'])]))
        self.seedbank.addSeed(self.seedbank.retrieve(0).research())
        self.assertEqual(len(self.seedbank.seedbank), 2)
        self.seedbank.clean()
        self.assertEqual(len(self.seedbank.seedbank), 1)

    def test_sum(self):
        self.seedbank.addSeeds([Seed([Gen(['a', 'a'])], researched=True), Seed([Gen(['a', 'a'])], researched=True)])
        self.seedbank.addSeeds(mate(self.seedbank.retrieve(0), self.seedbank.retrieve(0)))
        self.assertEqual(self.seedbank.sum(), 4)


if __name__ == "__main__":
    unittest.main()
