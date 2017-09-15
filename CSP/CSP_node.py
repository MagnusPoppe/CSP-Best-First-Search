import time

from a_star.node import Node
from nonogram.entry import Entry
from nonogram.puzzle import Puzzle


class CSPNode(Node):

    def __init__(self, parent, state : Puzzle, constraint=None):
        super().__init__(parent)

        # Hvordan skal state dette representeres?
        # - Liste med alle "entries"? Vanskelig å hashe.
        # - Brettet slik som det ser ut nå? Vanskelig å hashe.
        # - Puzzle( ) ?
        self.state = state # type: Puzzle

        # Dette blir selve regnestykket som skal utføres. Dette er
        # en funksjon. Lambdautrykk.
        if not constraint: constraint = self.constraint_maker
        self.make_constraint = constraint

        # Dette blir alle mulige noder som skal sjekkes. Neste "assumption".
        # Altså, noder som skal brukes med GAC algoritmen.
        self.children = self.generate_csps()  # type: list

    def __hash__(self):
        pass

    def constraint_maker(self, x, d, y):
        def constraint():
            return d <= y <= d+x
        return constraint

    def generate_csps(self):
        def generate(rows, columns):
            """ O(N6)... wow. """
            csp = []
            for row in rows: # type: Entry
                csp_queue = []
                for variable, variable_domain in row:
                    for domain in variable_domain:
                        # Nå ser vi på hvert enkelt domene med hver enkelt variabel:
                        for column in columns:
                            for individual_values in column.possibles:
                                for value in individual_values:         # Hver verdi i rekken av verdier.
                                    if value == 1: # kan kun være 0 eller 1.
                                       csp_queue += [self.make_constraint(variable, domain, value)]
                csp.append(csp_queue)
            return csp

        start = time.time()
        output = generate(self.state.rows, self.state.columns) + generate(self.state.columns, self.state.rows)
        print("Runtime for GenerateCSPS: " + str(time.time() - start) + " sec")
        print("Number of constraints:    " + str(len(output)))

        return output

    def create_children(self):
        pass

    def is_solution(self):
        pass # return self.h == 0

    def setF(self):
        """ Total weight of this node from start to end """
        pass

    def setH(self):
        """ Estimate of remaining weight to get to finish. """
        pass
