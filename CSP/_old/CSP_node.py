import time

from CSP._old.datastructure import Domain, Constraint
from CSP._old.datastructure import Variable
from a_star.node import Node
from nonogram.puzzle import Puzzle, Entry


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
        self.queue = self.generate_csps()  # type: list

    def __hash__(self):
        pass

    def constraint_maker(self, x, d, y):
        def constraint():
            return d <= y <= d+x
        return constraint

    def generate_csps(self) -> list:
        """
        Metoden genererer en nøstet liste som tilsvarer en CSP kø. Denne
        Køen inneholder en rekke funksjoner som skal representere en constraint.
        En CSP solver kan gå igjennom alle disse funksjonskallene og se om det
        er noen av dem som er ugyldige og kan fjernes.
        """

        def generate(rows, columns):
            """ O(N9)... wow. """
            csp = []
            for variables in rows: # type: Entry
                for variable in variables:  # type: Variable
                    for domain in variable.domain: # type: Domain
                        # Nå ser vi på hvert enkelt domene med hver enkelt variabel:
                        csp_queue = []
                        for other_variables in columns:
                            for other_variable in other_variables:
                                for other_domain in other_variable.domain:
                                    for _list in other_domain.possibles:
                                        for value in _list: # Hver verdi i rekken av verdier.
                                            if value == 1:  # kan kun være 0 eller 1.
                                                c = Constraint(
                                                    self.make_constraint(variable.value, domain.value, value),
                                                    [_list]
                                                )
                                                domain.constraints += [c]
        start = time.time()

        # Generating CSP:
        generate(self.state.rows, self.state.columns)
        generate(self.state.columns, self.state.rows)

        # Printing stats:
        print("Runtime for GenerateCSPS: " + str(time.time() - start) + " sec")
        queue = []
        for _list in self.state.rows + self.state.columns:
            queue += [entry for entry in _list]
        return queue

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
