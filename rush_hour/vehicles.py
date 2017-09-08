class Vehicle:
    """ A vehicle is a node used by a-star to win the game of rush hour. """

    HORIZONTAL = 0
    VERTICAL = 1

    FORWARDS = 0
    BACKWARDS = 1

    def __init__(self, x, y, orientation, size, identifier, special=False):
        # Coordinates for the top-left-corner of the object.
        self.x = x
        self.y = y
        self.id = identifier

        # Direction of the vehicle. Used for movement and
        self.orientation = orientation
        self.size = size
        self.special = special

    def __str__(self):
        if self.orientation == self.VERTICAL:
            orientation = "VERTICAL"
        else:
            orientation = "HORIZONTAL"
        return "at ("+str(self.x)+", "+str(self.y)+") in orientation " + orientation

    def spec(self) -> str:
        return str(self.orientation) + "," + str(self.x) + "," + str(self.y) + "," + str(self.size)

    def __eq__(self, other):
        """ True if all details match. """
        if not isinstance(other, Vehicle): return False

        return other.orientation == self.orientation \
           and other.x == self.x \
           and other.y == self.y \
           and other.size == self.size

    def get_moves(self, board) -> tuple:

        # Finds the next move:
        if self.orientation == self.VERTICAL:
            backwardX = self.x
            backwardY = self.y-1
            forwardX = self.x
            forwardY = self.y + self.size
        else:
            backwardX = self.x-1
            backwardY = self.y
            forwardX = self.x + self.size
            forwardY = self.y

        backward = (
            backwardX >= 0 and backwardY >= 0
            and board.board[backwardY][backwardX] == board.map_blank_space)
        forward = (
            forwardX < board.map_width and forwardY < board.map_height
            and board.board[forwardY][forwardX] == board.map_blank_space
        )

        if self.special and forwardX == 6 and forwardY == 2:
            return backward, True

        return backward, forward


"""
Created a specialized version of each type of vehicle to be able to
have the debugger display nicer names with "to string".
"""