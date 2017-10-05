import matrix
import tiles
from settings import *


class Map:
    m = None
    manager = {}

    def __init__(self, gridSize, name, tileSize=[32, 32], margin=[50, 50], fill=BLACK, add=True):
        if add:
            self.gridSize = gridSize  # Immutable
            self.tileSize = tileSize  # Can change, this represents default
            self.margin = margin  # Can change, this represents default

            self.name = name
            self.grid = matrix.Grid(self.gridSize, fill=tiles.Tile(fill))

            Map.manager[self.name] = self
            Map.m = self

    def load(self, mapname):
        Map.manager[Map.m.name] = Map.m
        Map.m = Map.manager[mapname]
