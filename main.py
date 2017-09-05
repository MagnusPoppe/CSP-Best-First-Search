import os

from a_star.agenda import Agenda
from a_star.core import AStarCore
from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board

map_folder = "/Users/MagnusPoppe/Desktop/OneDrive/Utvikling/appsPython/AI_project_1/maps"

def win_game(board):
    board1 = board.vehicles[0].make_move(1, board.copy())
    board1 = board1.vehicles[0].make_move(1, board1)
    board1 = board1.vehicles[4].make_move(0, board1)
    board1 = board1.vehicles[4].make_move(0, board1)
    board1 = board1.vehicles[3].make_move(1, board1)
    board1 = board1.vehicles[3].make_move(1, board1)
    board1 = board1.vehicles[3].make_move(1, board1)
    board1 = board1.vehicles[3].make_move(1, board1)
    board1 = board1.vehicles[4].make_move(1, board1)
    board1 = board1.vehicles[4].make_move(1, board1)
    board1 = board1.vehicles[5].make_move(1, board1)
    board1 = board1.vehicles[5].make_move(1, board1)

    board1 = board1.vehicles[0].make_move(0, board1)
    board1 = board1.vehicles[0].make_move(0, board1)
    board1 = board1.vehicles[0].make_move(0, board1)
    board1 = board1.vehicles[0].make_move(0, board1)

    return board.vehicles[0].make_move(0, board1)

if __name__ == '__main__':
    for filename in ["easy-3.txt", "medium-1.txt", "hard-3.txt", "expert-2.txt"]:
        file = open(os.path.join(map_folder, filename))
        file_to_string = ""
        for line in file: file_to_string += line
        file.close()

        board = Board(file_to_string)
        agenda = Agenda()
        agenda.enqueue(RushHourNode(board, parent=None))

        astar = AStarCore(agenda)
        winner_node = astar.best_first_search()
        print("RESULTS FOR FILE: " + filename)
        print("Game won with " + str(winner_node.f) + " moves.")
        print(astar.stats())
        # print(winner_node.parent.board)
        # print(winner_node.board)