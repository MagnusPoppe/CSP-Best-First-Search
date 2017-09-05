import os
from tkinter import Tk

import time

from a_star.agenda import Agenda
from a_star.core import AStarCore
from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board
from rush_hour.graphics import RushHourGUI

map_folder = "/Users/MagnusPoppe/Desktop/OneDrive/Utvikling/appsPython/AI_project_1/maps"

best_solution = [16, 24, 33, 73, 93]
minimum_nodes = [77, 611, 923, 5685, 24132]
files = ["easy-3.txt", "medium-1.txt", "hard-3.txt", "expert-2.txt", "expert-1.txt"]

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

    for i in range(len(files)):

        # Reading file:
        file = open(os.path.join(map_folder, files[i]))
        file_to_string = ""
        for line in file: file_to_string += line
        file.close()

        # Instantiating initial board and node:
        board = Board(file_to_string)
        agenda = Agenda()
        node = RushHourNode(board, parent=None)
        node.weight = 0
        agenda.enqueue(node)

        # Running A*:
        astar = AStarCore(agenda)
        winner_node = astar.best_first_search()

        # Printing stats:
        print("RESULTS FOR FILE: " + files[i])
        print("Game won with " + str(winner_node.g) + " moves. Best solution: " + str(best_solution[i]) + " moves.")
        print("Time used (seconds): " + str(astar.time_used()))
        print("Nodes generated: " + str(astar.total_nodes()) + " / " + str(minimum_nodes[i]) + " (BEST)")
        print("\nWinning board:")
        print(winner_node.board)
        print("\n")

        # Displaying result in gui:
        root = Tk()
        gui = RushHourGUI(root, files[i], winner_node)

        while gui.frameindex < len(gui.frames):
            root.update()
            gui.draw_board(gui.frames[gui.frameindex])
            time.sleep(.5)