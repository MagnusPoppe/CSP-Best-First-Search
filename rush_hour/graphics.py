import tkinter

import time

from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board


class RushHourGUI():

    colors = ["black", "green", "purple", "yellow", "orange", "blue", "pink", "cyan", "magenta", "salmon",
              "dark grey", "light grey", "maroon", "light yellow"]


    def __init__(self, title, speed=0.2, window_width=300, window_height=300):
        self.master = tkinter.Tk() # type: tkinter.Tk
        self.master.title(title)
        self.canvas_width = window_width
        self.canvas_height = window_height
        self.master.geometry('{}x{}'.format(self.canvas_width, self.canvas_height)) # Size of window.

        self.speed = speed
        self.colorassignment = {}
        self.frameindex = 0
        self.properly_initialized = False


    def assign_colors(self, node):
        self.properly_initialized = True
        for i in range(len(node.board.vehicles)):
            self.colorassignment[node.board.vehicles[i].id] = self.colors[i]


    def get_frames(self, node):
        if not node.parent: return [node.board]
        else:               return self.get_frames(node.parent) + [node.board]

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def draw_board(self, board: Board):
        self.clear()
        canvas = tkinter.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        canvas.pack()

        cell_height = self.canvas_height / board.map_height
        cell_width  = self.canvas_height / board.map_width

        for bY in range(board.map_height):
            for bX in range(board.map_width):
                cell = board.board[bY][bX]
                if cell == 0: continue
                x = (bX*cell_width)
                y = (bY*cell_height)
                canvas.create_rectangle(x, y, x+cell_width, y+cell_height, fill=self.colorassignment[cell])

        self.canvas = canvas
        self.frameindex += 1
        time.sleep(.2)
