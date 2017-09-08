import os

import copy

from rush_hour.vehicles import Vehicle


class Board():
    """
    This class represents a board configuration, freezed in time. The board
    does not move objects. For any object moved, the board can create a new board
    with the new configuration. The board can however check for possible moves for
    any given vehicle.
    """

    # Map information
    map_width  = 6
    map_height = 6
    map_blank_space = 0

    _left_up = 0
    _right_down = 1

    # List of vehicles on the map
    vehicles = []
    board = []

    # bool for won board:
    won = False


    def __init__(self, state: str):
        """ Reads a file containing the map and creates a complete map. """
        self.board = []        # self.board = [[self.map_blank_space] * self.map_height] * self.map_width
        self.vehicles = []
        self.state = state.strip("\n")

        for i in range(self.map_width):
            self.board.append([self.map_blank_space] * self.map_height)
        i = 0
        ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

        for line in state.split("\n"):
            if line == "": continue
            vehicle = Vehicle(line, ids[i], special=i==0)
            self.vehicles.append(vehicle)
            self._place_vehicle_on_board(vehicle)
            i += 1

    def __hash__(self):
        return hash(self.state)

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

    def __eq__(self, other) -> bool:
        " if same vehicles and same baord, they are equal. "

        if not isinstance(other, Board): return False

        for y in range(self.map_height):
            for x in range(self.map_width):
                if other.board[y][x] != self.board[y][x]:
                    return False

        if len(self.vehicles) != len(other.vehicles):
            return False

        for i in range(len(self.vehicles)):
            if other.vehicles[i] != self.vehicles[i]:
                return False

        return True

    def validate(self):
        map = {}
        for row in self.board:
            for tile in row:
                if tile not in map:
                    map[tile] = 0
                map[tile] += 1

        for id, count in map.items():
            for vehicle in self.vehicles:
                if id == vehicle.id and count != vehicle.size: return False
        return True

    def make_move(self, vehicle: Vehicle, direction):
        # Creating the modifier for vehicle coordinates:
        x = 0
        y = 0
        if vehicle.orientation == vehicle.VERTICAL:
            if direction == vehicle.FORWARDS:       y = 1
            elif direction == vehicle.BACKWARDS:    y = -1
        elif vehicle.orientation == vehicle.HORIZONTAL:
            if direction == vehicle.FORWARDS:       x = 1
            elif direction == vehicle.BACKWARDS:    x = -1

        state = ""
        for v in self.vehicles:
            if v.id == vehicle.id:
                state += str(vehicle.orientation) + ","
                state += str(vehicle.x+x) + ","
                state += str(vehicle.y+y) + ","
                state += str(vehicle.size) + "\n"
            else:
                state += v.spec + "\n"
        return Board(state)

    def _place_vehicle_on_board(self, vehicle: Vehicle):
        if (vehicle.special and vehicle.x == self.map_width-2 and vehicle.y == 2):
            self.won = True
            return

        if vehicle.orientation == vehicle.VERTICAL:
            self.board[vehicle.y][vehicle.x] = vehicle.id
            self.board[vehicle.y+1][vehicle.x] = vehicle.id
            if vehicle.size == 3: self.board[vehicle.y+2][vehicle.x] = vehicle.id
        elif vehicle.orientation == vehicle.HORIZONTAL:
            try:
                self.board[vehicle.y][vehicle.x] = vehicle.id
                self.board[vehicle.y][vehicle.x+1] = vehicle.id
                if vehicle.size == 3: self.board[vehicle.y][vehicle.x+2] = vehicle.id
            except Exception as e:
                pass

    def _place_vehicle_on_board_safe(self, vehicle: Vehicle):
        """ Places a vehicle on the map. Makes sure there is no
            overlapping vehicles.
        """
        # WIN CASE:
        if vehicle.special and vehicle.x == self.map_width-2 and vehicle.y == 2:
            self.won = True

        currentx = vehicle.x
        currenty = vehicle.y
        for i in range(vehicle.size):
            if i == 0:
                pass
            elif vehicle.orientation == vehicle.VERTICAL:
                currenty += 1
            elif vehicle.orientation == vehicle.HORIZONTAL:
                currentx += 1
            if self.board[currenty][currentx] == self.map_blank_space:
                self.board[currenty][currentx] = vehicle.id
            else:
                raise ValueError("Overlapping vehicles at coordiates ("+str(currentx)+", "+str(currenty)+") "
                                 "for vehicle " + str(vehicle))