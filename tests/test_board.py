import unittest

from rush_hour.board import Board
from rush_hour.vehicles import Truck, Car, SpecialCar


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board("easy-3.txt")

    def test_vehicle_types(self):
        self.assertTrue(isinstance(self.board.vehicles[1], Truck))
        self.assertTrue(isinstance(self.board.vehicles[0], Car))
        self.assertTrue(isinstance(self.board.vehicles[0], SpecialCar))

    def test_can_move(self):
        pass
        #left, right = board.get_moves(board.vehicles[1])

if __name__ == '__main__':
    unittest.main()