

class Color:
    def __init__(self, color):
        self.color = color

    def __add__(self, other):
        added = [0, 0, 0]
        for i in range(3):
            added[i] = self.color[i] + other.color[i]
            if added[i] > 255: added[i] = 255
        return Color(added)

    def __call__(self):
        return self.color

