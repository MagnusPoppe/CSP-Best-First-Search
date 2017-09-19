
class Variable:
    """ The variable class represents one single row or column. """

    def __init__(self, value, type, domain=None):
        self.value = value      # type: int
        self.domain = domain if domain else []
        self.map_domain = {}
        self.type = type

    def __str__(self):
        return str(self.value) + ": {" + ", ".join([str(dom) for dom in self.domain]) + "}"

    def delete(self, domain):
        del self.map_domain[domain.value]
        for i, dom in enumerate(self.domain):
            if dom == domain:
                del self.domain[i]
                break


class Domain:
    """
    The domain object exists so that we connect all objects
    together. This way, a change affects all objects with
    the connected data.

    Possibles are connected data. Each list inside the list is
    the same list as for every other domain object with the same
    variable parent.
    """

    def __init__(self, variable, value, possibles, constraints=None):
        # Peker til foreldre:
        self.variable = variable        # type: Variable

        # Domene verdier:
        self.value = value              # type: int
        self.possibles = possibles      # type: list(list(int))
        self.constraints = constraints if constraints else [] # type: list(lambda)

    def __str__(self):
        return str(self.value)

    def __del__(self):
        del self.variable
        del self.value
        del self.possibles
        del self.constraints

class Constraint:

    def __init__(self, func, affected_possibles):
        self.run = func
        self.possibles = affected_possibles

    def __del__(self):
        del self.run
        del self.possibles