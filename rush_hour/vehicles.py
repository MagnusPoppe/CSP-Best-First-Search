import copy


class Vehicle:
    """ A vehicle is a node used by a-star to win the game of rush hour. """

    HORIZONTAL = 0
    VERTICAL = 1

    FORWARDS = 0
    BACKWARDS = 1

    size = 0

    def __init__(self, x, y, orientation, identifier):
        # Coordinates for the top-left-corner of the object.
        self.x = x
        self.y = y
        self.id = identifier

        # Direction of the vehicle. Used for movement and
        self.orientation = orientation

    def __str__(self):
        if self.orientation == self.VERTICAL:
            orientation = "VERTICAL"
        else:
            orientation = "HORIZONTAL"
        return "at ("+str(self.x)+", "+str(self.y)+") in orientation " + orientation

    def __eq__(self, other):
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

        backward = False
        forward = False
        if backwardX >= 0 and backwardY >= 0 and board.board[backwardY][backwardX] == 0:
            backward = True

        if forwardX < board.map_width and forwardY < board.map_height and board.board[forwardY][forwardX] == 0:
            forward = True

        return backward, forward

    def make_move(self, direction: int, board):
        backwards, forwards = self.get_moves(board)

        if direction == self.FORWARDS and forwards:
            drawX, drawY, newX, newY = self._calculate_forwards_move()
            eraseX = self.x
            eraseY = self.y
        elif direction == self.BACKWARDS and backwards:
            drawX, drawY, eraseX, eraseY = self._calculate_backwards_move()
            newX = drawX
            newY = drawY
        elif direction < 0 or 1 <= direction:
            raise ValueError("Illegal directional value. Value was " + str(direction))

        # Copying board to avoid reference errors:
        new_board = board.copy()  # TODO: Find better solution.

        # Moving the vehicle on the board
        new_board.board[drawY][drawX] = self.id
        new_board.board[eraseY][eraseX] = board.map_blank_space

        # Updating the vehicle with new coordnates
        self.x = newX
        self.y = newY

        return new_board

    def _calculate_forwards_move(self):

        # Finding where forwards is according to direction:
        if self.orientation == self.VERTICAL:
            forwardX = self.x
            forwardY = self.y + self.size
            new_vehicle_position_x = self.x
            new_vehicle_position_y = self.y +1

        else: # Horizontal
            forwardX = self.x + self.size
            forwardY = self.y
            new_vehicle_position_x = self.x +1
            new_vehicle_position_y = self.y

        return forwardX, forwardY, new_vehicle_position_x, new_vehicle_position_y

    def _calculate_backwards_move(self):

        # Finding where forwards is according to direction:
        if self.orientation == self.VERTICAL:
            backwardsX = self.x
            backwardsY = self.y -1
            eraseX = self.x
            eraseY = self.y + self.size-1

        else: # Horizontal
            backwardsX = self.x -1
            backwardsY = self.y
            eraseX = self.x + self.size-1
            eraseY = self.y

        return backwardsX, backwardsY, eraseX, eraseY

class Truck(Vehicle):
    size = 3

    def __init__(self, x, y, orientation, identifier):
        super().__init__(x, y, orientation, identifier)

    def __str__(self):
        return "Truck " + self.id + " " + super().__str__()

class Car(Vehicle):
    size = 2

    def __init__(self, x, y, orientation, identifier):
        super().__init__(x, y, orientation, identifier)

    def __str__(self):
        return "Car " + self.id + " " + super().__str__()

class SpecialCar(Car):
    def __init__(self, x, y, orientation, identifier):
        super().__init__(x, y, orientation, identifier)

    def __str__(self):
        return "Special " + super().__str__()