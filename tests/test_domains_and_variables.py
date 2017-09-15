import os
import unittest
from itertools import permutations, product

from file_tostring import read_file_to_string
from nonogram.main import files, file_folder
from nonogram.puzzle import Puzzle


class TestDomainsAndVariables(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_boards = [read_file_to_string(os.path.join(file_folder, file)) for file in files][:3]
        cls.puzzles = [Puzzle(b) for b in cls.all_boards]

    def setUp(self): pass

    def test_correct_dimensions_of_board(self):
        file = self.all_boards[0].split("\n")
        puzzle = Puzzle(self.all_boards[0])
        first_line = file[0].split(" ")
        self.assertEqual(puzzle.w, int(first_line[0]), "Not correct width of board.")
        self.assertEqual(puzzle.h, int(first_line[1]), "Not correct height of board.")

        # Rows and columns
        self.assertEqual(len(puzzle.columns), int(first_line[0]), "Not correct width of board.")
        self.assertEqual(len(puzzle.rows), int(first_line[1]), "Not correct height of board.")

    def test_create_tuple(self):
        total = 0
        for i, puzzle in enumerate(self.puzzles):
            for entry in puzzle.rows + puzzle.columns:
                possibilities = []
                possibilities += entry.get_all_possibilities(entry.domains)

                number_of_possibilities = len(entry.domains[0])
                self.assertTrue(number_of_possibilities >= 1, "No possible solutions found.")
                for domain in entry.domains[1:]:
                    number_of_possibilities *= len(domain)

                self.assertEqual(len(possibilities), number_of_possibilities)
                total += number_of_possibilities

if __name__ == '__main__':
    unittest.main()