import matrix
import tiles
from settings import *


class Map:
    m = None  # Represents currently selected map
    manager = {}  # Keeps track of all maps

    def __init__(self, gridSize, name, tileSize=[32, 32], margin=[50, 50], fill=BLACK):
        self.gridSize = gridSize  # You can't change this without destroying everything
        self.tileSize = tileSize  # Can change, this represents default, you will need to rescale textures
        self.margin = margin  # Can change, this represents default

        self.name = name
        self.grid = matrix.Grid(self.gridSize, fill=tiles.Tile(fill))

        Map.manager[self.name] = self
        Map.m = self

    def load(self, mapname):
        Map.manager[Map.m.name] = Map.m
        Map.m = Map.manager[mapname]
