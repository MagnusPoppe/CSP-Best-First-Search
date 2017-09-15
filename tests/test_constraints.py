import os
import unittest

from file_tostring import read_file_to_string
from nonogram.main import files, file_folder
from nonogram.puzzle import Puzzle


class TestDomains(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_boards = [read_file_to_string(os.path.join(file_folder, file)) for file in files][:3]
        cls.puzzles = [Puzzle(b) for b in cls.all_boards]

    def test_astar_gac(self):
        def todo_revise():
            pass

        def domain_filter(queue):
            while queue:
                todo = queue.pop(0)
                if todo_revise(todo):
                    # push(children)
                    pass


        queue = []