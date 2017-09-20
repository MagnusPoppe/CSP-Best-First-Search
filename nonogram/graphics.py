import tkinter

import time

from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board


class NonogramGUI():

    colors = ["black", "green", "purple", "yellow", "orange", "blue", "pink", "cyan", "magenta", "salmon",
              "dark grey", "light grey", "maroon", "light yellow"]


    def __init__(self, title, speed=0.2, window_width=300, window_height=300):
        self.master = tkinter.Tk() # type: tkinter.Tk
        self.master.title(title)
        self.canvas_width = window_width
        self.canvas_height = window_height
        self.master.geometry('{}x{}'.format(self.canvas_width, self.canvas_height)) # Size of window.

        self.speed = speed
        self.frameindex = 0
        self.properly_initialized = True

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def draw_board(self, board):
        self.clear()
        canvas = tkinter.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        canvas.pack()

        cell_height = self.canvas_height / len(board)
        cell_width  = self.canvas_height / len(board[0])

        for bY, list in enumerate(board):
            for bX in range(len(list)):
                cell = board[bY][bX]
                if cell == " ": continue
                x = (bX*cell_width)
                y = (bY*cell_height)
                canvas.create_rectangle(x, y, x+cell_width, y+cell_height, fill=self.colors[-5])

        self.canvas = canvas
        self.frameindex += 1
        time.sleep(self.speed)
