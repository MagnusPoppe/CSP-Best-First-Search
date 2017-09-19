class CSP:

    def __init__(self, variable, domain, constraint):
        # Variable (x) is the value to be tested for the constraint.
        self.x = variable

        # Domain (d) are the possible states that are allowed.
        self.d = domain # type: list

        # Constraint (c) is the rule that makes the game able to be solved.
        self.c = constraint

    def __str__(self):
        return "{" + str(self.x) + ": " + str(self.d) + "}"

class NonoLengthCSP(CSP):
    """
    Variable (x) is the value to be tested for the constraint. For Nonograms, a variable is
    any of the pictured numbers on either the start of a row or the start of a column.

    Domain (d) are the possible placements for the nonograms entry numbers. for each number
    here is a set of possible placement starts. Domain is a list of those start indexes.

    Constraint (c) is the function that enforces the domain is correctly used.
    """

    # Constraint to check that in one row, a variable is placed legally
    # besides its neighbour.
    # y+1 because of the needed space between rules.
    row_consistancy_constraint = lambda current, size, next: \
        current + size < next + 1

    def __init__(self, x:int, d: list, row_index: int, columns:list):
        super().__init__(x, d, self.row_consistancy_constraint)
        self.i = row_index
        self.columns = columns
