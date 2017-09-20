class Datastructure:

    def __init__(self, filespecs=None):
        rows   = []
        cols   = []
        width  = 0
        height = 0

        if filespecs: rows, cols, width, height = self.read_game_specs(filespecs)

        self.row_length = width
        self.col_length = height
        self.rows = rows # type: list(Var)
        self.cols = cols # type: list(Var)
        self._create_by_lists()

    def __hash__(self):
        return hash(self._hash_code)

    def set_rows_cols(self, rows=None, cols=None, row_len=0, col_len=0):
        self.rows = rows
        self.row_length = row_len
        self.cols = cols
        self.col_length = col_len
        self._create_by_lists()

    def _create_by_lists(self):
        def sort(by_data):

            for i, list in by_data.items():
                if len(list) > 1:
                    continue
                for i in range(len(list)):
                    for j in range(i, len(list)):
                        if list[i].domain[0] > list[j].domain[0]:
                            temp = list[i]
                            list[i] = list[j]
                            list[j] = temp
        self.by_row = {}
        for row in self.rows:
            if row.index not in self.by_row: self.by_row[row.index] = []
            self.by_row[row.index].append(row)


        self.by_col = {}
        for col in self.cols:
            if col.index not in self.by_col: self.by_col[col.index] = []
            self.by_col[col.index].append(col)

        sort(self.by_row)
        sort(self.by_col)

    def generate_hash(self):
        self._hash_code = ""
        for i, elements in self.by_row.items():
            for element in elements: self._hash_code += str(element)
        for i, elements in self.by_col.items():
            for element in elements: self._hash_code += str(element)

    def read_game_specs(self, filespecs):

        def generate_domains(constants, rowlen):
            domains = []
            for i, variable in enumerate(constants):
                max_behind = 0 if i == 0 else sum(constants[:i - 1]) + i + 1
                max_infront = rowlen - sum(constants[i + 1:]) - 1 if len(constants) - 1 > i else rowlen
                domain = []
                unexplored = max_behind
                while (unexplored + variable <= max_infront):
                    domain.append(unexplored)
                    unexplored += 1

                domains.append(domain)
            return domains

        lines = filespecs.split("\n")
        w = int(lines[0].split(" ")[0])
        h = int(lines[0].split(" ")[1])
        rows = []
        cols = []

        def specs_to_var(constants, type, domains, index):
            output = []
            for i in range(len(constants)):
                const = constants[i]
                domain = domains[i]
                output.append(Var(const, domain, index, type ))
            return output

        index = 0
        for i in range(h, 0, -1):
            constants = [int(element) for element in lines[i].split()]
            rows += specs_to_var(constants, Var.ROW, generate_domains( constants, w ), index)
            index += 1
        index = 0
        for i in range(h + 1, h + w + 1):
            constants = [int(element) for element in lines[i].split()]
            cols += specs_to_var(constants, Var.COL, generate_domains( constants, h ), index)
            index += 1

        return rows, cols, w, h

    def __len__(self):
        return len(self.rows) + len(self.cols)

    def draw_solution(self):
        board = [ [" "] * self.row_length for i in range(self.col_length)]
        if all([len(val.domain) == 1 for val in self.rows + self.cols]):
            for row in self.rows:
                start = row.domain[0]
                stop = row.domain[0]+row.constant
                for i in range(start, stop):
                    board[row.index][i] = "X"

        return board

    def draw_as_is(self):
        board = [ [" "] * self.row_length for i in range(self.col_length)]
        for row in self.rows:
            if len(row.domain) == 1:
                start = row.domain[0]
                stop = row.domain[0]+row.constant
                for i in range(start, stop):
                    board[row.index][i] = "X"
        for row in self.cols:
            if len(row.domain) == 1:
                start = row.domain[0]
                stop = row.domain[0]+row.constant
                for i in range(start, stop):
                    board[i][row.index] = "X"
        return board

class Var:

    ROW = 0
    COL = 1

    def __init__(self, value:int, domain:list, index:int, type:int):
        self.constant = value   # type: int
        self.domain = domain    # type: list(int)
        self.type = type
        self.index = index

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str(self.constant) + "{" + ",".join([str(d) for d in self.domain]) + "}"

    def __cmp__(self, other): return len(self.domain) - len(other.domain)
    def __lt__(self, other): return self.__cmp__(other) < 0
    def __le__(self, other): return self.__cmp__(other) < 0 or self.__cmp__(other) == 0
    def __gt__(self, other): return self.__cmp__(other) > 0
    def __ge__(self, other): return self.__cmp__(other) > 0 or self.__cmp__(other) == 0

    def __eq__(self, other):
        return self.constant == other.constant \
           and self.domain == other.domain \
           and self.type == other.type \
           and self.index == other.index

    def __len__(self):
        return len(self.domain)