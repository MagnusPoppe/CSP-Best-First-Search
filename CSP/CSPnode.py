import sys
from copy import deepcopy

import time

from CSP.GAC import GAC
from CSP.state import State, Variable
from a_star.node import Node


class GACNode(Node):

    weight = 1

    def __init__(self, parent, state):
        self.state = GAC(state)  # type: State
        self.children = []
        super().__init__(parent)
        self.setF()
        self.board = state.printable()

    def __hash__(self):
        return hash(self.state)

    def create_children(self):
        def find_optimal_domain(_list):
            """
            Finds the optimal domain to assume a value for. The optimal
            domain contains as few as possible values, but more than 2.
            2 is the optimal value.
            """
            candidate = sys.maxsize
            min = sys.maxsize
            for i, entry in enumerate(_list):
                if len(entry.domain) < 2:
                    continue
                elif len(entry.domain) == 2:
                    return i
                if min > len(entry.domain):
                    candidate = i
                    min = len(entry.domain)
            return candidate

        if self.h == 0: return [] # 0 if no variable has a domain bigger size 1

        # Deciding what list to use:
        _list = self.state.rows
        if sum( [len(row.domain) -1 for row in self.state.rows] ) == 0:
            _list = self.state.cols

        # Finding the optimal candidate to assume for.
        candidate = find_optimal_domain(_list)
        if candidate < len(_list):
            assume = _list[ candidate ]
        else: return []

        # An assumtion is made for each of the domain values.
        for domain_value in assume.domain:

            # Copying state for use with new node.
            new_state = State(rows=deepcopy(self.state.rows),
                              cols=deepcopy(self.state.cols),
                              constraints=self.state.constraints)
            # Overwriting the old variable with the assumed one:
            if assume.type == new_state.TYPE_ROW:
                new_state.rows[assume.index] = Variable(assume.index, [domain_value], assume.type)
            elif assume.type == new_state.TYPE_COL:
                new_state.cols[assume.index] = Variable(assume.index, [domain_value], assume.type)

            # Creating child node
            self.children += [ GACNode(self, new_state) ]

        return self.children

    def is_solution(self):
        return self.h == 0

    def setF(self):
        """ Total weight of this node from start to end """
        if self.parent: self.f = self.setG(self.parent.g) + self.setH()
        else: self.f = self.setG() + self.setH()
        return self.f

    def setH(self):
        """ Estimate of remaining weight to get to finish. """
        self.h = sum([len(elem.domain)-1 for elem in self.state.rows + self.state.cols])
        return self.h

