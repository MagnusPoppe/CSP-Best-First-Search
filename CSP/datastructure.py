
class Variable:
    """ The variable class represents one single row or column. """

    def __init__(self, value, domain=None):
        self.value = value      # type: int
        self.domain = domain if domain else []
        self.map_domain = {}

    def __str__(self):
        return str(self.value) + ": {" + ", ".join([str(dom) for dom in self.domain]) + "}"

class Domain:
    """
    The domain object exists so that we connect all objects
    together. This way, a change affects all objects with
    the connected data.

    Possibles are connected data. Each list inside the list is
    the same list as for every other domain object with the same
    variable parent.
    """

    def __init__(self, variable, value, possibles, constraints):
        # Peker til foreldre:
        self.variable = variable        # type: Variable

        # Domene verdier:
        self.value = value              # type: int
        self.possibles = possibles      # type: list(list(int))
        self.constraints = constraints  # type: list(lambda)

    def __str__(self):
        return str(self.value)