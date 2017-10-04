# Grid class for my game
import copy


class Grid:
    def __init__(self, size, fill=int):
        self.width, self.height = size
        self.matrix = [[copy.copy(fill) for y in range(self.height)] for x in range(self.width)]

    def get(self, x, y):
        return self.matrix[x][y]

    def put(self, x, y, value):
        self.matrix[x][y] = copy.copy(value)

    def show(self):
        print(self.matrix)

    def star(self, x, y, r):
        """Selects a star shaped (square rotated 45 degrees) area"""
        for lx in range(-r, r+1):
            for ly in range(-r + abs(lx), r - abs(lx) + 1):
                yield x+lx, y+ly, self.get(x+lx, y+ly)

    def rect(self, x, y, w, h):
        """Selects a rectangular area"""
        for lx in range(x, x+w):
            for ly in range(y, y+h):
                yield lx, ly, self.get(lx, ly)

    def line(self, x1, y1, x2, y2):
        """Bresenham's line algorithm"""
        err = abs(y2 - y1 / x2 - x1)
        error = 0.0
        y = y1
        for x in range(x1, x2):
            yield x, y, self.get(x, y)
            error += err
            if error >= 0.5:
                y += 1
                error -= 1

    def all(self):
        """Selects everything within the matrix"""
        return self.rect(0, 0, self.width, self.height)

    def fill(self, func, value):
        """Fills the selected area with one value"""
        for i in func:
            self.put(i[0], i[1], value)

    def search(self, func, variable, value):
        """Accepts both generator functions and lists"""
        for i in func:
            if getattr(i[2], variable) == value:
                yield i
