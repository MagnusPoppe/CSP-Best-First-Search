
"""
Not sure if a python priority queue is the correct datastructure for this.
Create your own for prioritizing correctly or find a way to use the
default python priority queue comparator or ints.
"""
from a_star.node import Node


class Agenda():
    # Since both datastructures will reference the same nodes,
    # the space used will not be too bad. Speed increase for
    # using the hashmap is huge.

    def __init__(self):
        self._queue = []
        self._map = {}

    def __str__(self):
        return "Agenda with " + str(len(self._queue)) + " nodes."

    def __len__(self):
        return len(self._queue)

    def __contains__(self, item) -> bool:
        """ Checks if a node is in the agenda using the hashmap. """
        if isinstance(item, Node):
            return hash(item) in self._map
        return False


    def enqueue(self, node: Node):
        """
        Sets a node into queue for the priority list. Also
        adds a node to the hashmap.
        """
        if not isinstance(node, Node): raise TypeError("Agenda does not support " + str(node) + ".")
        # self._queue.insert(0,node)
        self._queue.append(node)
        self._queue.sort() # Uses the comparator in the Node class.
        self._map[hash(node)] = node

    def dequeue(self) -> Node:
        """
        Takes the next node out of queue, and removes it from the hashmap.
        :return: Next node to be evaluated.
        """
        node = self._queue.pop(0)
        try: del self._map[hash(node)]
        except KeyError: pass
        return node

    def get_node(self, hash) -> Node:
        return self._map[hash]

    def remove_node(self, node: Node):
        self._map[hash(node)] = None
        self._queue.remove(node)

    def is_empty(self) -> bool:
        """ Checks for empty agenda. True if empty. """
        return len(self._queue) == 0