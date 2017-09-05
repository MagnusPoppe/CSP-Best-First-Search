import math

from a_star.node import Node


class RushHourNode(Node):

    board = None

    def __init__(self, board, parent):
        super().__init__(parent)
        self.weight = 1 # In rush hour a move is always 1. therefore, weight of node is 1.
        self.board = board
        self.setF() # Also sets G and H.

    def __hash__(self):
        return hash(self.board)

    def setH(self):
        self.h = self.manhatten_distance()
        # self.h = self.euclidiean_distance()
        # self.h = self.weighted_path_distance()
        return self.h

    def setF(self):
        self.f = self.setG() + self.setH()

    def manhatten_distance(self) -> int:
        """ Manhatten distance, absolute value of x to goal + y to goal. """
        return 5 - self.board.vehicles[0].x # Y is not included since the car only moves on x axis.

    def euclidiean_distance(self) -> float:
        """ Pythagoras sentence for distance """
        return math.sqrt(math.pow(5-self.board.vehicles[0].x, 2) + math.pow( 2 - self.board.vehicles[0].y , 2))

    def weighted_path_distance(self) -> int:
        # Points to earn
        empty_space = 1
        vehicle_in_space = 2

        score = 0
        vehicle = self.board.vehicles[0]

        # Looping through the squares in front of the car to weigh the path
        for xi in range(vehicle.x+vehicle.size, 5):
            score += empty_space if self.board.board[vehicle.y][xi] == self.board.map_blank_space else vehicle_in_space

        return score

    def is_solution(self) -> bool:
        return self.board.won

    def create_children(self) -> list:
        self.children = []

        # Checking for each vehicle if they can make either a backwards or
        # forwards move:
        for vehicle in self.board.vehicles:
            backwards, forwards = vehicle.get_moves(self.board)

            # If a move can be made, the child node is created and saved.
            if forwards:
                board_f = self.board.make_move(vehicle, vehicle.FORWARDS)
                if board_f is not None:
                    self.children.append(RushHourNode(board_f, self))
            if backwards:
                board_b = self.board.make_move(vehicle, vehicle.BACKWARDS)
                if board_b is not None:
                    self.children.append(RushHourNode(board_b, self))

        return self.children

