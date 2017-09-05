import math

from a_star.node import Node


class RushHourNode(Node):

    board = None

    def __init__(self, board, parent):
        super().__init__(parent)
        self.board = board
        self.setF() # Also sets G and H.

    def __hash__(self):
        return hash(self.board)

    def setH(self):
        self.h = self.euclidiean_distance()
        return self.h

    def setF(self):
        self.f = self.setG() + self.setH()

    def manhatten_distance(self):
        return 5 - self.board.vehicles[0].x

    def euclidiean_distance(self):
        return math.sqrt(math.pow(5-self.board.vehicles[0].x, 2) + math.pow( 2 - self.board.vehicles[0].y , 2))

    # def path_distance(self):
    #     seen = {}
    #     def find_goal(x, y, depth):
    #         if (x, y) in seen or x < 0 or x > 5 or y < 0 or y > 5:
    #             return None
    #
    #         if x == 5 and y == 2:
    #             return depth
    #
    #         seen[(x, y)] = 1
    #         results = []
    #
    #         if x <= 4 and self.board.board[x+1][y] == self.board.map_blank_space:                     # Forward
    #             res = find_goal(x+1, y, depth=depth+1)
    #             if res: results.append(res)
    #         if x <= 4 and y <= 4 and self.board.board[x + 1][y + 1] == self.board.map_blank_space:    # Diagonal down
    #             res = find_goal(x-1, y-1, depth=depth+2)
    #             if res: results.append(res)
    #         if x <= 4 and 1 <= y and self.board.board[x + 1][y - 1] == self.board.map_blank_space:    # Diagonal up
    #             res = find_goal(x-1, y-1, depth=depth+2)
    #             if res: results.append(res)
    #         if y <= 4 and self.board.board[x][y+1] == self.board.map_blank_space:                     # Down
    #             res = find_goal(x, y+1, depth=depth+1)
    #             if res: results.append(res)
    #         if 1 <= y and self.board.board[x][y-1] == self.board.map_blank_space:                     # Up
    #             res = find_goal(x, y+1, depth=depth+1)
    #             if res: results.append(res)
    #
    #         if not results and x > 0:
    #             res = find_goal(x, y+1, depth=depth+1)
    #             if res: results.append(res)
    #
    #         return min(results) if results else None
    #
    #     res = find_goal(self.board.vehicles[0].x, self.board.vehicles[0].y, depth=0)
    #     return res




    def weight(self):
        """ In rush hour a move is always 1. therefore, weight of node is 1. """
        return 1

    def is_solution(self):
        return self.h == 0

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

