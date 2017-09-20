import os
import unittest

from CSP._old._GACNode import Datastructure, GACNode
from a_star.agenda import Agenda
from a_star.core import AStarCore
from file_tostring import read_file_to_string
from nonogram.graphics import NonogramGUI
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
            child_H = sum([len(elem) for elem in child_node.state.rows + child_node.state.cols])

            self.assertNotEqual(hash(node), hash(child_node), "Different nodes have same hash..")
            self.assertEqual( len(child_node.state), len(node.state), "Nodes should always have same number of variables.")
            self.assertTrue(node_H >= child_H, "New node should have smaller H than parent.")

    def test_hash_code(self):
        node = GACNode(None, self.example_puzzle)
        othernode = GACNode(None, self.example_puzzle)
        children = node.create_children()
        otherchildren = othernode.create_children()

        # All children should have the same hashcode as they are based on the same nodes.
        for i in range(len(children)):
            self.assertEqual(hash(children[i]), hash(otherchildren[i]))

        self.assertEqual(hash(node), hash(othernode))

        # Dive deep:
        self.assertEqual(hash(children[0].parent), hash(otherchildren[0].parent))
        gen_2_children = children[0].parent.create_children()
        for i in range(len(children)):
            self.assertEqual(hash(gen_2_children[i]), hash(otherchildren[i]), children[i])



    def test_queue(self):
        node = GACNode(None, self.example_puzzle)
        state = node.state
        node.is_solution()
        self.assertEqual(state, node.state, "State changed after running GAC.")
        print("\n".join([str(e) for e in node.state.draw_solution()]))

        self.assertTrue(not all([len(val.domain) == 1 for val in node.state.rows + node.state.cols]),
                        "All domains are now narrowed down to length 1 when they should not be.")

        print("DONE ANALYZING QUEUE.")

    def test_x_gac_astar(self):
        node = GACNode(None, self.example_puzzle)
        agenda = Agenda()
        agenda.enqueue(node)
        Astar = AStarCore(agenda, displaymode=True, gui=NonogramGUI("SEARCH...", speed=0))
        winner = Astar.best_first_search()
        self.assertFalse(winner is None, "Winner-node not found.")
        print("\n".join([str(e) for e in winner.domain_filtered_state.draw_solution()]))

if __name__ == '__main__':
    unittest.main()