
class State():

    TYPE_ROW = 0
    TYPE_COL = 1

    def __init__(self, file_input=None, rows=None, cols=None, constraints=None):
        self.cols = [] if cols is None else cols
        self.rows = [] if cols is None else rows

        if file_input:
            self.read_file(file_input)
            print("Initial state created from file!")

        self.constraints = self.make_constraints() if constraints is None else constraints

    def __hash__(self):
        return hash("".join([e.concat_string() for e in self.cols + self.rows]))

    def make_constraints(self):

        def factory(x, y):
            def constraint(v1type, v1, v2):
                if v1type == self.TYPE_ROW:
                    return v1[y] == v2[x]
                return v2[y] == v1[x]
            return constraint

        output = []
        for x, row in enumerate(self.rows):
            for y, col in enumerate(self.cols):
                output += [Constraint(x, y, factory(x=x, y=y))]
        return output

    def printable(self):
        output = [[" "]*len(self.cols) for y in range(len(self.rows))]
        for col in self.cols:
            if len(col.domain) == 1:
                for tup in col.domain:
                    for y, char in enumerate(tup):
                        if char == "1":
                            output[y][col.index] = "X"
                        else:
                            output[y][col.index] = " "

        # for row in self.rows:
        #     if len(row.domain) == 1:
        #         for tup in row.domain:
        #             for x, char in enumerate(tup):
        #                 if char == "1":
        #                     output[ row.index ][x] = "X"
        return output

    def read_file(self, file):

        def f(r, n, t, acc=[]):
            if t == 0:
                if n <= 0: yield acc
                return
            for x in r:
                if x > n: break
                for lst in f(r, n - x, t - 1, acc + [x]):
                    yield lst

        lines = file.split("\n")
        w = int(lines[0].split(" ")[0])
        h = int(lines[0].split(" ")[1])

        def constant_toString(const, current, length):
            r = "1"*int(const)
            if current < len(length)-1:
                r += "0"
            return r

        def permuatations_of_constants(all_constants, length):
            all = []
            for row in all_constants:
                leng = sum([len(const) for const in row])
                diff = length - leng
                permutations = [x for x in f(range(diff + 1), diff, len(row) + 1)]

                all_permutations = []
                for permutation in permutations:
                    output = ""
                    for i, value in enumerate(permutation):
                        output += "0" * value
                        if i < len(permutation) - 1:
                            output += row[i]
                    all_permutations.append(output)
                all.append( all_permutations )
            return all
        # Rows
        rows = []
        for i in range(h, 0, -1):
            row_input = lines[i].split()
            const = [constant_toString(constant, j, row_input) for j, constant in enumerate(row_input)]
            rows.append(const)

        rows = permuatations_of_constants(rows, w)
        # Cols
        cols = []
        for i in range(h + 1, h + w + 1):
            col_input = lines[i].split()
            const = [constant_toString(constant, j, col_input) for j, constant in enumerate(col_input)]
            cols.append(const)

        cols = permuatations_of_constants(cols, h)
        for i, col in enumerate(cols):
            self.cols.append(Variable(i, col, self.TYPE_COL))
        for i, row in enumerate(rows):
            self.rows.append(Variable(i, row, self.TYPE_ROW))
        #
        #
        #
        # for col in cols:
        #     leng = sum([len(const) for const in col])
        #     diff = w - leng
        #     pass

class Variable():

    def __init__(self, index, domain, type):
        self.index = index   # type: int
        self.type  = type    # type: int
        self.domain = domain # type: list

    def __str__(self):
        return ("ROW" if self.type == 0 else "COLUMN") + " " + str(self.index) +\
                ". domain-values=" + str(len(self.domain)) + ""

    def concat_string(self):
        return " ".join(self.domain)


class Constraint():

    def __init__(self, x, y, func):
        self.x = x
        self.y = y
        self.func = func

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"