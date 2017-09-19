from copy import copy

from CSP.GAC import GAC
from a_star.node import Node


class GACNode(Node):

    def __init__(self, parent, state):
        self.state = state
        self._state_hash_string = " - ".join([str(x) for x in self.state.rows + self.state.cols])
        super().__init__(parent)

        pass

    def __hash__(self):
        return hash(self._state_hash_string)

    def create_children(self):
        """
        Takes out a Var from the list of rows or cols from state.
        The var taken out will have its domain split up into single
        values.
        :return:
        """
        if all([len(element.domain) == 1 for element in self.state.rows]):
            sorted_list = copy(self.state.cols)
            other       = copy(self.state.rows)
            type = Var.COL
        else:
            sorted_list = copy(self.state.rows)
            other       = copy(self.state.cols)
            type = Var.ROW


        sorted_list.sort()
        # TODO Fix the problem. Node is not poped from sorted_list.
        smallest = sorted_list.pop(0)

        children = []
        for variable in smallest.domain:
            x = Var(smallest.constant, [variable], smallest.index, smallest.type)
            state = Datastructure()
            row = [x] + sorted_list if type == Var.COL else other
            col = other             if type == Var.COL else [x] + sorted_list
            state.set_rows_cols(row, col, self.state.row_length, self.state.col_length)

            children += [GACNode(self, state)]

        # TODO: NO CHILDREN ARE CREATED
        # Because todo.revise removes all domain-values.

        self.children = children
        return children

    def is_solution(self):
        """ If all Var elements have a domain of length 1. """

        queue = self.create_revise_queue()
        solution = GAC(queue)
        return solution and all([len(e.domain) == 1 for e in self.state.rows + self.state.cols])

    def setF(self):
        """ Total weight of this node from start to end """
        pass

    def setH(self):
        """ Estimate of remaining weight to get to finish. """
        return sum([len(elem) for elem in self.state.rows + self.state.cols])

    def create_revise_queue(self):
        ### HER QUEUES ALLE OBJEKTER FOR TODO-REVISE ALGORITMEN.
        def enqueue_diff_direction(direction, by_other):
            queue = []
            for col in direction: # type: Var
                for dom in col.domain:
                    for i in range(dom, dom+col.constant):
                        for row in by_other[i]:

                            queue += [(copy(col), copy(row))]
            return queue

        def enqueue_same_direction(by):
            queue = []
            for i, entries in by.items():
                if len(entries) > 1:
                    prev = entries[0]
                    for entry in entries[1:]:
                        queue += [ (copy(prev), copy(entry)) ]
                        prev = entry
            return queue

        return enqueue_same_direction(self.state.by_row) \
             + enqueue_same_direction(self.state.by_col) \
             + enqueue_diff_direction(self.state.cols, self.state.by_row) \
             + enqueue_diff_direction(self.state.rows, self.state.by_col)



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

    def set_rows_cols(self, rows, cols, row_len, col_len):
        self.rows = rows
        self.row_length = row_len

        self.cols = cols
        self.col_length = col_len

        self._create_by_lists()


    def _create_by_lists(self):
        self.by_row = {}
        for row in self.rows:
            if row.index not in self.by_row: self.by_row[row.index] = []
            self.by_row[row.index].append(row)
        self.by_col = {}
        for col in self.cols:
            if col.index not in self.by_col: self.by_col[col.index] = []
            self.by_col[col.index].append(col)

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

class Var:

    ROW = 0
    COL = 1

    def __init__(self, value:int, domain:list, index:int, type:int):
        self.constant = value   # type: int
        self.domain = domain    # type: list(int)
        self.type = type
        self.index = index

    def __str__(self):
        return str(self.constant) + "{" + ",".join([str(d) for d in self.domain]) + "}"

    def __cmp__(self, other):
        return len(self.domain) - len(other.domain)

    def __eq__(self, other): return self.__cmp__(other) == 0
    def __lt__(self, other): return self.__cmp__(other) < 0
    def __le__(self, other): return self.__cmp__(other) < 0 or self.__cmp__(other) == 0
    def __gt__(self, other): return self.__cmp__(other) > 0
    def __ge__(self, other): return self.__cmp__(other) > 0 or self.__cmp__(other) == 0

    def __len__(self):
        return len(self.domain)