import os

from rush_hour.vehicles import Car, Truck, SpecialCar, Vehicle


class Board():
    """
    This class represents a board configuration, freezed in time. The board
    does not move objects. For any object moved, the board can create a new board
    with the new configuration. The board can however check for possible moves for
    any given vehicle.
    """

    # Map information
    _map_folder = "/Users/MagnusPoppe/Desktop/OneDrive/Utvikling/appsPython/AI_project_1/maps"
    _map_width  = 6
    _map_height = 6

    _left_up = 0
    _right_down = 1

    # List of vehicles on the map
    vehicles = []
    board = []


    def __init__(self, filename: str):
        """ Reads a file containing the map and creates a complete map. """

        for i in range(self._map_width):
            self.board.append([0]*self._map_height)

        with open(os.path.join(self._map_folder, filename)) as file:
            i = 0
            ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M","N"]
            for line in file:
                vehicle = self._create_vehicle(line.strip("\n").split(","), ids[i])
                self.vehicles.append(vehicle)

                self._place_vehicle_on_board(vehicle)
                i += 1

    def __str__(self):
        output = ""
        for row in self.board:
            for cell in row:
                if not cell:
                    output += "  "
                else:
                    output += str(cell) + " "
            output += "\n"
        return output

    def get_moves(self, vehicle: Vehicle) -> tuple:

        # Finds the next move:
        if vehicle.orientation == vehicle.VERTICAL:
            beforeX = vehicle.x
            beforeY = vehicle.y-1
            afterX = vehicle.x
            afterY = vehicle.y + vehicle.size
        else:
            beforeX = vehicle.x-1
            beforeY = vehicle.y
            afterX = vehicle.x + vehicle.size
            afterY = vehicle.y

        before = False
        after = False
        if beforeX >= 0 and beforeY >= 0 and self.board[beforeY][beforeX] == 0:
            before = True

        if afterX < self._map_width and afterY < self._map_height and self.board[afterY][afterX] == 0:
            after = True

        return before, after



    def _place_vehicle_on_board(self, vehicle: Vehicle):
        """ Places a vehicle on the map. Makes sure there is no
            overlapping vehicles.
        """

        currentx = vehicle.x
        currenty = vehicle.y
        for i in range(vehicle.size):
            if i == 0:
                pass
            elif vehicle.orientation == vehicle.VERTICAL:
                currenty += 1
            elif vehicle.orientation == vehicle.HORIZONTAL:
                currentx += 1

            if self.board[currenty][currentx] == 0:
                self.board[currenty][currentx] = vehicle.id
            else:
                raise ValueError("Overlapping vehicles at coordiates ("+str(currentx)+", "+str(currenty)+")")

    def _create_vehicle(self, info: list, id:str) -> Vehicle:
        """ Creates a vehicle from an array of specs.
            as specified in the task, the information about a given vehicle is formatted
            as follows:
            [ Orientation, X, Y, Size ]
        """
        orientation = int(info[0])
        x = int(info[1])
        y = int(info[2])
        size = int(info[3])

        if len(self.vehicles) == 0 and size == 2:
            vehicle = SpecialCar(x, y, orientation, id)
        elif size == 2:
            vehicle = Car(x, y, orientation, id)
        elif size == 3:
            vehicle = Truck(x, y, orientation, id)
        else:
            raise ValueError("No vehicle matching the description in the file for vehicle: " + str(info))

        return vehicle