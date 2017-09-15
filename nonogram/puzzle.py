from nonogram.entry import Entry

class Puzzle():

    def __init__(self, spec):
        lines = spec.split("\n")

        self.spec = spec
        first_line = lines[0].split(" ")
        self.w = w = int(first_line[0])
        self.h = h = int(first_line[1])
        self.grid = [[0] * h for i in range(w)]
        self.rows = [Entry(lines[i].split(), w) for i in range(h, 0, -1)]
        self.columns = [Entry(lines[i].split(), h) for i in range(h + 1, h + w + 1)]
