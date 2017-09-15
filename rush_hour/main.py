import cProfile
import os
from tkinter import Tk

import time

import sys

from a_star.agenda import Agenda
from a_star.core import AStarCore
from a_star.rush_hour_node import RushHourNode
from file_tostring import read_file_to_string
from rush_hour.board import Board
from rush_hour.graphics import RushHourGUI

map_folder = "/Users/MagnusPoppe/Google Drive/Utvikling/appsPython/AI_project_1/rush_hour/maps"

best_solution = [16, 24, 33, 73, 93]
minimum_nodes = [77, 611, 923, 5685, 24132]
files = ["easy-3.txt", "medium-1.txt", "hard-3.txt", "expert-2.txt", "expert-1.txt"]
heuristics = ["Manhatten", "Euclidiean", "Weighted path", "all-in-front"]


def display_results(solution, title):
    # Displaying result in gui:
    gui = RushHourGUI(title, speed=0.3)
    frames = gui.get_frames(solution)
    gui.assign_colors(solution)
    while gui.frameindex < len(frames):
        gui.master.update()
        gui.draw_board(frames[gui.frameindex])

best = {}
def record_best(file, heuristic, moves, time, analyzed, total_nodes):
    if not file in best:
        best[file] = {
            "moves": {"stat": sys.maxsize, "heuristic": ""},
            "time": {"stat": sys.maxsize, "heuristic": ""},
            "nodes-analyzed": {"stat": sys.maxsize, "heuristic": ""},
            "total-nodes": {"stat": sys.maxsize, "heuristic": ""}
        }
    moves = moves-1
    if moves < best[file]["moves"]["stat"]:
        best[file]["moves"]["stat"] = moves
        best[file]["moves"]["heuristic"] = heuristic

    if time < best[file]["time"]["stat"]:
        best[file]["time"]["stat"] = time
        best[file]["time"]["heuristic"] = heuristic

    if analyzed < best[file]["nodes-analyzed"]["stat"]:
        best[file]["nodes-analyzed"]["stat"] = analyzed
        best[file]["nodes-analyzed"]["heuristic"] = heuristic

    if total_nodes < best[file]["total-nodes"]["stat"]:
        best[file]["total-nodes"]["stat"] = total_nodes
        best[file]["total-nodes"]["heuristic"] = heuristic

def print_stats(file, heuristic, node, time, analyzed, total_nodes):
    print("RESULTS FOR FILE:    " + file)
    print("Heuristic algorithm: " + heuristic)
    print("Time used (seconds): " + str(time))
    print("Steps to solution:   " + str(node.g-1) + " / " + str(best_solution[i]) + " (BEST)")
    print("Nodes expanded:      " + str(analyzed))
    print("Nodes generated:          " + str(total_nodes) + " / " + str(minimum_nodes[i]) + " (BEST)")
    print("\n")

def print_best_stats(file):
    stats = best[file]
    print("For file " + file)
    print("Least nodes generated: " + stats["total-nodes"]["heuristic"] +
          " @ " + str(stats["total-nodes"]["stat"]))
    print("Least nodes analyzed:  " + stats["nodes-analyzed"]["heuristic"] +
          " @ " + str(stats["nodes-analyzed"]["stat"]))
    print("Best time:             " + stats["time"]["heuristic"] +
          " @ " + str(stats["time"]["stat"]))
    print("\n")

def run(file, heuristic=0):
    astar = None

    # Teardown:
    if astar:
        astar.reset()
        board = None
        node = None
        winner_node = None

    # Reading file:
    input = read_file_to_string(os.path.join(map_folder, file))

    # Instantiating initial board and node:
    board = Board(input)
    agenda = Agenda()
    node = RushHourNode(board, parent=None, heuristic=heuristic)
    node.setF()
    node.weight = 0
    agenda.enqueue(node)

    # Running A*:
    astar = AStarCore(agenda, displaymode=False)
    winner_node = astar.best_first_search()

    # Printing stats:
    print_stats(file, heuristics[heuristic], winner_node, astar.time_used(), astar.nodes_analyzed(), astar.total_nodes())
    record_best(file, heuristics[heuristic], winner_node.g, astar.time_used(), astar.nodes_analyzed(), astar.total_nodes())

    return winner_node

if __name__ == '__main__':
    file = None
    use_gui = False
    if len(sys.argv) == 3:
        use_gui = len(sys.argv) > 1 and sys.argv[1] == "-gui"
        file = sys.argv[2]
    elif len(sys.argv) == 2:
        use_gui = len(sys.argv) > 1 and sys.argv[1] == "-gui"
        if not use_gui: file = sys.argv[1]

    heuristic_algorithm = 3

    if file:
        winner_node = run(file, heuristic_algorithm)
        # print_best_stats(file)
        if use_gui: display_results(winner_node, file)
    else:
        for i in range(len(files)):
            winner_node = run(files[i], heuristic_algorithm)
            # print_best_stats(files[i])
            if use_gui: display_results(winner_node, files[i])
