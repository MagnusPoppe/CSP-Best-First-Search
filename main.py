import os
from tkinter import Tk

import time

import sys

from a_star.agenda import Agenda
from a_star.core import AStarCore
from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board
from rush_hour.graphics import RushHourGUI

map_folder = "/Users/MagnusPoppe/Desktop/OneDrive/Utvikling/appsPython/AI_project_1/maps"

best_solution = [16, 24, 33, 73, 93]
minimum_nodes = [77, 611, 923, 5685, 24132]
files = ["easy-3.txt", "medium-1.txt", "hard-3.txt", "expert-2.txt", "expert-1.txt"]

def display_results(solution, title):
    # Displaying result in gui:
    root = Tk()
    gui = RushHourGUI(root, title, winner_node)
    while gui.frameindex < len(gui.frames):
        root.update()
        gui.draw_board(gui.frames[gui.frameindex])
        time.sleep(.2)

if __name__ == '__main__':
    use_gui = len(sys.argv) > 1 and sys.argv[1] == "-gui"
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
        node.heuristic_function = node.euclidiean_distance
        node.weight = 0
        agenda.enqueue(node)

        # Running A*:
        astar = AStarCore(agenda)
        winner_node = astar.best_first_search()

        # Printing stats:
        print("RESULTS FOR FILE:    " + files[i])
        print("Moves used:          " + str(winner_node.g) + " / " + str(best_solution[i]) + " (BEST)")
        print("Time used (seconds): " + str(astar.time_used()))
        print("Nodes analyzed:      " + str(astar.nodes_analyzed()) )
        print("Nodes seen:          " + str(astar.total_nodes()) + " / " + str(minimum_nodes[i]) + " (BEST)")
        print("\nWinning board:")
        print(winner_node.board)
        print("\n")

        if use_gui: display_results(winner_node, files[i])