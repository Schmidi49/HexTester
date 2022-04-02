from functools import partial

prnt = partial(print, sep='', end='')

TYPE_DEFAULT = 0
PERSON = 1
OBJECT = 2

UP = 1
DOWN = -1
LEFT = -1
CENTER = 0
RIGHT = 1

class Field:
    def __init__(self, c, r):
        self.COLS = c
        self.ROWS = r
        self.hexes = [[[None] * r for i in range(c)] for j in range(2)]

    def __str__(self):
        s = "  " + "     ---  " * self.COLS + "\n"
        s += "  " + "    /   \\ " * self.COLS + "\n   "

        for i in range(self.COLS): s += "  / " + self.valueAsField(True, i, self.ROWS - 1, 0) + " \\ "
        s += "\n"
        for i in range(self.COLS): s += "  ---  " + self.valueAsField(True, i, self.ROWS - 1, 1)
        s += "\n"
        for i in range(self.COLS): s += " /   \\ " + self.valueAsField(True, i, self.ROWS - 1, 2)
        s += " /\n"

        for i in range(self.COLS): s += "/ " + self.valueAsField(False, i, self.ROWS - 1, 0) + " \\   "
        s += "/\n"
        for i in range(self.COLS): s += "  " + self.valueAsField(False, i, self.ROWS - 1, 1) + "  ---"
        s += "\n"
        for i in range(self.COLS): s += "\\ " + self.valueAsField(False, i, self.ROWS - 1, 2) + " /   "
        s += "\\\n"

        for j in range(2, self.ROWS):
            for i in range(self.COLS): s += " \\   / " + self.valueAsField(True, i, self.ROWS - j, 0)
            s += " \\\n"
            for i in range(self.COLS): s += "  ---  " + self.valueAsField(True, i, self.ROWS - j, 1)
            s += "\n"
            for i in range(self.COLS): s += " /   \\ " + self.valueAsField(True, i, self.ROWS - j, 2)
            s += " /\n"

            for i in range(self.COLS): s += "/ " + self.valueAsField(False, i, self.ROWS - j, 0) + " \\   "
            s += "/\n"
            for i in range(self.COLS): s += "  " + self.valueAsField(False, i, self.ROWS - j, 1) + "  ---"
            s += "\n"
            for i in range(self.COLS): s += "\\ " + self.valueAsField(False, i, self.ROWS - j, 2) + " /   "
            s += "\\\n"

        for i in range(self.COLS): s += " \\   / " + self.valueAsField(True, i, 0, 0)
        s += " \\\n"
        for i in range(self.COLS): s += "  ---  " + self.valueAsField(True, i, 0, 1)
        s += "\n /   "
        for i in range(self.COLS): s += "\\ " + self.valueAsField(True, i, 0, 2) + " /   "
        s += " \n"

        for i in range(self.COLS): s += "/ " + self.valueAsField(False, i, 0, 0) + " \\   "
        s += "/\n"
        for i in range(self.COLS): s += "  " + self.valueAsField(False, i, 0, 1) + "  ---"
        s += "\n"
        for i in range(self.COLS): s += "\\ " + self.valueAsField(False, i, 0, 2) + " /   "
        s += "\n"

        s += " \\   /    " * self.COLS + "\n"
        s += "  ---     " * self.COLS + "\n"

        return s

    def __getitem__(self, cord):
        return self.hexes[cord[0]][cord[1]][cord[2]]

    def __setitem__(self, cord, value):
        self.hexes[cord[0]][cord[1]][cord[2]] = value

    def clear(self):
        for i in self.COLS:
            for j in self.ROWS:
                self.hexes[False][i][j] = None
                self.hexes[True][i][j] = None

    def validHex(self, cords):
        return cords[1] < self.COLS and cords[2] < self.ROWS

    def hexIsEmpty(self, cords):
        return self.hexes[cords[0]][cords[1]][cords[2]] is None

    def valueAsField(self, w, x, y, row):
        value = self.hexes[w][x][y]
        if value is None:
            return "   "
        value = str(value)
        length = len(value)
        if length == 0:
            return "   "
        elif length == 1:
            if row == 1:
                return ' ' + value + ' '
        elif length < 4:
            if row == 1:
                value += (3 - length) * ' '
                return value
        else:
            value += (9 - length) * ' '
            return value[3 * row:3 * row + 3]
        return "   "

    def print(self):
        print(self.__str__())


class Coordinate:
    def __init__(self, w=False, x=0, y=0):
        self.w = w
        self.x = x
        self.y = y

    def __getitem__(self, item):
        if item == 0:
            return self.w
        if item == 1:
            return self.x
        if item == 2:
            return self.y
        return KeyError

    def __str__(self):
        return str(self.x) + (".5, " if self.w else ", ") + str(self.y) + ".5" if self.w else ""

    def __neg__(self):
        return Coordinate(self.w, -self.x - self.w, -self.y - self.w)

    def __add__(self, other):
        return Coordinate(self.w ^ other.w,
                          self.x + other.x + (self.w & other.w),
                          self.y + other.y + (self.w & other.w))

    def __sub__(self, other):
        return self + other.__neg__()



    def __mul__(self, other):
        if type(other) is int:
            w = self.w and other % 2 == 0
            if other > 0:
                x = self.x // 2 + 1
                y = self.y // 2 + 1
            else:
                x = self.x // -2
                y = self.y // -2
            return Coordinate(w, x, y)
        else:
            raise TypeError("Coordinate can only be multiplied by integers")


class Piece:
    def __init__(self, field=None, name="default", type=0, cords=None):
        self.TYPE = type
        self.name = name

        if isinstance(field, Field) or field is None:
            self.field = field
        else:
            raise ValueError("Invalid type of attribute field")
        if isinstance(cords, Coordinate):
            self.place(cords)
        elif cords is None:
            self.coordinates = None
        else:
            raise ValueError("Invalid type of attribute coordinate")

    def __str__(self):
        return self.name

    def place(self, cords):
        if isinstance(self.field, Field):
            if self.coordinates is None:
                if self.field.validHex(cords):
                    self.coordinates = cords
                    self.field[cords] = self
                else:
                    raise ValueError("Coordinates are not in the field")
            else:
                raise ReferenceError("Piece is already placed")
        else:
            raise ReferenceError("Piece has no valid Field")

    def remove(self):
        if isinstance(self.field, Field):
            if self.coordinates is None:
                raise ReferenceError("Piece is not placed")
            else:
                self.field[self.coordinates] = None
                self.coordinates = None
        else:
            raise ReferenceError("Piece has no valid Field")

    def isPlaced(self):
        if isinstance(self.field, Field) and self.coordinates is not None and self == self.field[self.coordinates]:
            return True
        return False

    def step(self, orientation, direction):
        test = Coordinate(direction != 0, direction // 2, (orientation + (direction == 0)) // 2)
        destination = self.coordinates + test

        if self.field.validHex(destination):
            if self.field.hexIsEmpty(destination):
                self.field[destination] = self
                self.field[self.coordinates] = None
                self.coordinates = destination
                return True
        return False






