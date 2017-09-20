import os
from time import sleep

import sys

from CSP.CSPnode import GACNode
from CSP.state import State
from a_star.agenda import Agenda
from a_star.core import AStarCore
from file_tostring import read_file_to_string
from nonogram.graphics import NonogramGUI

file_folder = "/Users/MagnusPoppe/Google Drive/Utvikling/appsPython/AI_project_1/nonogram/boards"
files = [
    "nono-example.txt",
    "nono-cat.txt",
    "nono-chick.txt",
    "nono-clover.txt",
    "nono-elephant.txt",
    "nono-fox.txt",
    "nono-rabbit.txt",
    "nono-sailboat.txt",
    "nono-snail2.txt",
    "nono-telephone.txt",
    "nono-reindeer.txt",
 ]

if __name__ == '__main__':
    for file in files[-6:-5]:
        print("\nCalculating " + file)
        _initial_state = State(read_file_to_string(os.path.join(file_folder, file)))

        use_gui = False
        display_mode = False
        if len(sys.argv) == 3:
            use_gui = len(sys.argv) > 1 and sys.argv[1] == "-gui"
            display_mode = sys.argv[2] == "-displaymode"
        elif len(sys.argv) == 2:
            use_gui = len(sys.argv) > 1 and sys.argv[1] == "-gui"
            if not use_gui: file = sys.argv[1]


        # INITIALIZING A*
        agenda = Agenda()
        astar = AStarCore(agenda, displaymode=display_mode, gui=NonogramGUI("Nonogram: " + file))
        agenda.enqueue( GACNode(None, _initial_state) )
        solution = astar.best_first_search()

        print("DONE IN "+str(round(astar.time_used(), 4)) +" sec")

    sleep(60)