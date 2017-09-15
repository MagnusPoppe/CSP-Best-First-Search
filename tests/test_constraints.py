import os
import unittest

from CSP.CSP_node import CSPNode
from file_tostring import read_file_to_string
from nonogram.main import files, file_folder
from nonogram.puzzle import Puzzle


class TestDomains(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_boards = [read_file_to_string(os.path.join(file_folder, file)) for file in files][:3]
        cls.puzzles = [Puzzle(b) for b in cls.all_boards]

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
        self.assertTrue( y > 0, "None of the domain values could be removed.")
        pass