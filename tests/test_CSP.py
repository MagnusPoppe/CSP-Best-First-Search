import os
import unittest

from CSP.GACNode import Datastructure, GACNode
from a_star.agenda import Agenda
from a_star.core import AStarCore
from file_tostring import read_file_to_string
from nonogram.main import file_folder, files

class TestCSP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_boards = [read_file_to_string(os.path.join(file_folder, file)) for file in files][:3]
        cls.example_puzzle = Datastructure(cls.all_boards[0])

    def test_datastructure(self):
        self.assertTrue(len(self.example_puzzle.rows) > 0)
        self.assertTrue(len(self.example_puzzle.cols) > 0)

    def test_node(self):
        node = GACNode(None, self.example_puzzle)
        child_nodes = node.create_children()
        node_H = sum([len(elem) for elem in node.state.rows + node.state.cols])
        for child_node in child_nodes:
            self.assertNotEqual(hash(node), hash(child_node))
            child_H = sum([len(elem) for elem in child_node.state.rows + child_node.state.cols])
            self.assertEqual( len(child_node.state), len(node.state), "Nodes should always have same number of variables.")
            self.assertTrue(node_H >= child_H, "New node should have smaller H than child.")

    def test_hash_code(self):
        node = GACNode(None, self.example_puzzle)
        othernode = GACNode(None, self.example_puzzle)
        # self.assertEqual(hash(node), hash(othernode))

    def test_queue(self):
        node = GACNode(None, self.example_puzzle)
        state = node.state
        node.is_solution()
        self.assertEqual(state, node.state, "State changed after running GAC.")
        print("\n".join([str(e) for e in node.state.draw_solution()]))

        self.assertTrue(not all([len(val.domain) == 1 for val in node.state.rows + node.state.cols]),
                        "All domains are now narrowed down to length 1 when they should not be.")

    def test_gac_astar(self):
        node = GACNode(None, self.example_puzzle)
        agenda = Agenda()
        agenda.enqueue(node)
        Astar = AStarCore(agenda, displaymode=False)
        winner = Astar.best_first_search()
        self.assertNotEqual(winner, None, "Winner-node not found.")

if __name__ == '__main__':
    unittest.main()