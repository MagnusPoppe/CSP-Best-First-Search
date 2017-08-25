import unittest

from rush_hour.board import Board
from rush_hour.vehicles import Truck, Car, SpecialCar


class TestBoard(unittest.TestCase):

    def setUp(self):
        pass

    def test_vehicle_types(self):
        board = Board("easy-3.txt")
        self.assertTrue(isinstance(board.vehicles[1], Truck))
        self.assertTrue(isinstance(board.vehicles[0], Car))
        self.assertTrue(isinstance(board.vehicles[0], SpecialCar))


    def test_can_move(self):
        board = Board("easy-3.txt")

        left, right = board.get_moves(board.vehicles[1])
if __name__ == '__main__':
    unittest.main()