class Vehicle:
    """ A vehicle is a node used by a-star to win the game of rush hour. """

    HORIZONTAL = 0
    VERTICAL = 1

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