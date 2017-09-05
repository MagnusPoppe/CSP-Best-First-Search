

class Node():
    # Values used in A star to prioritize nodes:
    f = None
    g = None
    h = None
    weight = 0

    # Parent and children needs to be connected:
    parent = None
    children = []

    def __init__(self, parent):
        self.parent = parent # type: Node

    def __hash__(self):
        pass


    # Implemented methods to support compare and default comparator:
    def __cmp__(self, other):
        return self.f - other.f

    def __eq__(self, other): return self.__cmp__(other) == 0
    def __lt__(self, other): return self.__cmp__(other) < 0
    def __le__(self, other): return self.__cmp__(other) < 0 or self.__cmp__(other) == 0
    def __gt__(self, other): return self.__cmp__(other) > 0
    def __ge__(self, other): return self.__cmp__(other) > 0 or self.__cmp__(other) == 0

    def create_children(self):
        pass

    def is_solution(self):
        pass # return self.h == 0

    def recalculate_G_for_all_children(self, new_parent):
        """ TODO: Gives recursion error. """
        self.parent = new_parent
        self.setG(new_parent.g)
        for child in self.children:
            child.recalculate_G_for_all_children(self)

    def setF(self):
        """ Total weight of this node from start to end """
        pass

    def setG(self, parent_value=None):
        """
        Total weight from start to this node
        :param parent_value: to avoid unnesseary recursion
        :return: g(x)
        """
        if isinstance(parent_value, int):
            self.g = parent_value + self.weight
        elif self.parent:
            self.g = self.parent.setG() + self.weight
        else:
            self.g = self.weight

        return self.g

    def setH(self):
        """ Estimate of remaining weight to get to finish. """
        pass
