import os
import unittest

from CSP import CSPNode
from CSP import revise, GAC_loop
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



    def test_revise_algorithm(self):
        puzzle = self.puzzles[0] # Example puzzle.
        x = CSPNode(None, puzzle)

        initial = len(x.state.rows[0][0].domain)
        # HVA GÅR INN HER?!
        revise(x.state.rows[0][0])
        self.assertTrue(initial > len(x.state.rows[0][0].domain), "No changes in domain when changes should happen.")

        count = 0
        while x.state.rows:
            variables = x.state.rows.pop(0)
            for variable in variables:
                if revise(variable):
                   count += 1

    def test_GAC_loop(self):
        puzzle = self.puzzles[0] # Example puzzle.
        x = CSPNode(None, puzzle)
        if (GAC_loop(x.queue)):
            y=2
        else:
            y=1

    def test_CSP_node(self):

        puzzle = self.puzzles[0] # Example puzzle.

        x = CSPNode(None, puzzle)
        length = sum([len(child) for child in x.children])
        # self.assertEqual(len(x.children), puzzle.w + puzzle.h)

        t = 0
        y = 0
        # Counting True/False values:
        for child in x.children:
            temp_t = 0
            while child:
                constraint = child.pop(0)
                temp_t += 1 if constraint() else 0
            if temp_t == 0:
                y += 1
            t += temp_t
        # self.assertTrue( y > 0, "None of the domain values could be removed.")
        pass

if __name__ == '__main__':
    unittest.main()