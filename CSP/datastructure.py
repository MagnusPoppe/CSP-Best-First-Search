
class Variable:

    def __init__(self, value, domain):
        self.value = value      # type: int
        self.domain = domain    # type: list(Domain)


class Domain:

    def __init__(self, variable, value, possibles, constraints):
        # Peker til foreldre:
        self.variable = variable        # type: Variable

        # Domene verdier:
        self.value = value              # type: int
        self.possibles = possibles      # type: list(list)
        self.constraints = constraints  # type: list(lambda)
