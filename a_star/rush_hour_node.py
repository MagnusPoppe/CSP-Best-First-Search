import math

from a_star.node import Node


class RushHourNode(Node):

    board = None

    def __init__(self, board, parent, heuristic=None):
        super().__init__(parent)
        self.weight = 1 # In rush hour a move is always 1. therefore, weight of node is 1.
        self.board = board
        self.heuristic_algorithm = heuristic
        self.setF()  # Also sets G and H.

    def __hash__(self):
        return hash(self.board)

    def setH(self):
        if   self.heuristic_algorithm == 0: self.h = self.manhatten_distance()
        elif self.heuristic_algorithm == 1: self.h = self.euclidiean_distance()
        elif self.heuristic_algorithm == 2: self.h = self.weighted_path_distance()
        elif self.heuristic_algorithm == 3: self.h = self.all_infront_distance()
        return self.h

    def setF(self):
        if self.parent: self.f = self.setG(self.parent.g) + self.setH()
        else: self.f = self.setG() + self.setH()
        return self.f

    def manhatten_distance(self) -> int:
        """ Manhatten distance, absolute value of x to goal + y to goal. """
        return 5 - self.board.vehicles[0].x # Y is not included since the car only moves on x axis.

    def euclidiean_distance(self) -> float:
        """ Pythagoras sentence for distance """
        return self.pythagoras_sentence(self.board.vehicles[0].x,5,2,self.board.vehicles[0].y )

    def pythagoras_sentence(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

    def weighted_path_distance(self) -> int:
        """
        Gives a heurisitc based on all squares in the path of the vehicle.
        Points are given for the contents of each cell in front of the vehicle:
        Empty cell          = 1
        Vehicle in the cell = 2
        :return: heuristic
        """
        # Points to earn
        empty_space = 1
        vehicle_in_space = 2

        score = 0
        vehicle = self.board.vehicles[0]

        # Looping through the squares in front of the car to weigh the path
        for xi in range(vehicle.x+vehicle.size, 5):
            score += empty_space if self.board.board[vehicle.y][xi] == self.board.map_blank_space else vehicle_in_space

        return score

    def all_infront_distance(self) -> int:
        """
        Gives a heurisitc based on all squares infront of the vehicle.
        Points are given for the contents of each cell in the grid:
        Empty cell          = 1
        Vehicle in the cell = 2

        # NOT ADMISSABLE.
        :return: heuristic
        """

        # Points to earn
        empty_space = 1
        vehicle_in_space = 2
        score = 0

        # Looping through the squares
        for xi in range(self.board.vehicles[0].x + self.board.vehicles[0].size, 5):
            for y in range(self.board.map_height):
                _point = empty_space if self.board.board[y][xi] == self.board.map_blank_space else vehicle_in_space
                score += _point
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
                    self.children.append(RushHourNode(board_f, self, self.heuristic_algorithm))
            if backwards:
                board_b = self.board.make_move(vehicle, vehicle.BACKWARDS)
                if board_b is not None:
                    self.children.append(RushHourNode(board_b, self, self.heuristic_algorithm))

        return self.children

