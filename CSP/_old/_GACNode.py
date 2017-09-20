import sys
from copy import deepcopy

from CSP._old.GAC import GAC
from CSP._old.old_State import Datastructure
from CSP._old.old_State import Var
from a_star.node import Node


class GACNode(Node):

    weight = 1

    def __init__(self, parent, state):
        self.state = state
        queue = self.create_revise_queue(self.state)
        self.solution = GAC(queue)
        self.state.generate_hash()
        super().__init__(parent)
        self.setF()
        self.board = self.state.draw_as_is()

    def __hash__(self):
        # TODO NOT WORKING.
        return hash(self.state)

    def create_children(self):
        """
        Takes out a Var from the list of rows or cols from state.
        The var taken out will have its domain split up into single
        values.
        :return:
        """
        if all([len(element.domain) == 1 for element in self.state.rows]):
            main  = self.state.cols
            other = self.state.rows
            type = Var.COL
        else:
            main  = self.state.rows
            other = self.state.cols
            type = Var.ROW

        # There is no point in
        minimal = sys.maxsize
        small = sys.maxsize
        for i in range(len(main)):
            if (minimal > len(main[i]) and len(main[i]) > 1):
                minimal = len(main[i])
                small = i

        try:
            smallest = main[small]
        except IndexError:
            return []

        children = []

        for variable in smallest.domain:
            x = Var(smallest.constant, [variable], smallest.index, smallest.type)
            state = Datastructure()
            if type == Var.ROW:
                row = deepcopy(main)
                row[small] = x
                col = deepcopy(other)
            else:
                col = deepcopy(main)
                col[small] = x
                row = deepcopy(other)
            state.set_rows_cols(rows=row, cols=col, row_len=self.state.row_length, col_len=self.state.col_length)

            children += [GACNode(self, state)]

        self.children = children
        return children

    def is_solution(self):
        """ If all Var elements have a domain of length 1. """

        # all_domains_is_1 = all( [len(e.domain) == 1 for e in self.domain_filtered_state.rows + self.domain_filtered_state.cols] )
        h = self.h == 0
        return h and self.solution

    def setF(self):
        """ Total weight of this node from start to end """
        if self.parent: self.f = self.setG(self.parent.g) + self.setH()
        else: self.f = self.setG() + self.setH()
        return self.f

    def setH(self):
        """ Estimate of remaining weight to get to finish. """
        self.h = sum([len(elem)-1 for elem in self.state.rows + self.state.cols])
        return self.h

    def create_revise_queue(self, state):
        ### HER QUEUES ALLE OBJEKTER FOR TODO-REVISE ALGORITMEN.
        def enqueue_diff_direction(direction, by_other):
            queue = []
            for col in direction: # type: Var
                for dom in col.domain:
                    for i in range(dom, dom+col.constant):
                        for row in by_other[i]:
                            queue += [ (col, row) ]
            return queue

        def enqueue_same_direction(by):
            queue = []
            for i, entries in by.items():
                if len(entries) > 1:
                    prev = entries[0]
                    for entry in entries[1:]:
                        queue += [ (prev, entry) ]
                        prev = entry
            return queue

        # Using the domain filtered state insted of the state object because the state should be immutable.
        return enqueue_diff_direction(state.cols, state.by_row)\
             + enqueue_diff_direction(state.rows, state.by_col) \
             + enqueue_same_direction(state.by_col) \
             + enqueue_same_direction(state.by_row) \
