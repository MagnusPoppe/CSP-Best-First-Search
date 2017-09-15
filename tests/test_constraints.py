import os
import unittest

from CSP.CSP_node import CSPNode
from file_tostring import read_file_to_string
from nonogram.main import files, file_folder
from nonogram.puzzle import Puzzle


class TestDomains(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_boards = [read_file_to_string(os.path.join(file_folder, file)) for file in files]
        cls.puzzles = [Puzzle(b) for b in cls.all_boards]

    def test_CSP_node(self):
        puzzle = self.puzzles[0] # Example puzzle.

        x = CSPNode(None, puzzle)
        f = sum([len(child) for child in x.children])
        self.assertEqual(len(x.children), puzzle.w + puzzle.h)

        t = 0
        # Counting True/False values:
        for child in x.children:
            while child:
                constraint = child.pop(0)
                t += 1 if constraint() else 0
        f = f - t
        pass