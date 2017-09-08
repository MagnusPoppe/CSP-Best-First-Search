from nonogram.nano_entry import NanoEntry


class NonogramBoard():
    untouched = 0
    open = 1
    closed = 2

    def __init__(self, spec: str):
        lines = spec.split("\n")

        self.spec    = spec
        self.h  = int(spec[0])
        self.w  = int(spec[2])
        self.grid    = [[0] * self.w for i in range(self.h)]
        self.rows    = [NanoEntry( lines[i].split() ) for i in range(1, self.h)]
        self.columns = [NanoEntry( lines[i].split() ) for i in range(self.h, self.h + self.w)]

    def __hash__(self):
        string = ""
        for y in range(self.h):
            string += "".join(str(elem) for elem in self.grid[y])
        return hash(self.spec)

    def __str__(self):
        string = ""
        for y in range(self.h):
            string += " ".join(str(elem) for elem in self.grid[y]) + "\n"
        return string

    def mark(self, x:int, y:int, mark:int):
        self.grid[y][x] = mark

    def peek(self, x, y):
        return self.grid[y][x]