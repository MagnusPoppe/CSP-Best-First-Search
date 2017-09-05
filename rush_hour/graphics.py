import tkinter

from a_star.rush_hour_node import RushHourNode
from rush_hour.board import Board


class RushHourGUI():

    colors = ["blue", "green", "purple", "yellow", "orange", "pink", "cyan", "magenta", "salmon", "grey", "light grey", "maroon", "light yellow"]
    canvas_width = 400
    canvas_height = 400

    def __init__(self, master, title, winner_node):
        self.master = master # type: tkinter.Tk
        self.colorassignment = {}
        for i in range(len(winner_node.board.vehicles)):
            self.colorassignment[winner_node.board.vehicles[i].id] = self.colors[i]


        master.title(title)
        master.geometry('{}x{}'.format(self.canvas_width, self.canvas_height)) # Size of window.
        self.frameindex = 0
        self.frames = self.get_frames(winner_node)

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