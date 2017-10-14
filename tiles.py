import pygame
import math
import textures
from ui import Error
from maps import *
from settings import *


class Tile:
    window = pygame.display.set_mode((1, 1))

    texture = textures.Texture()

    # When I need to rescale the overlays
    overlayList = []

    def __init__(self, image, drawOutline=True, outlineColor=DARKGREY, outlineWidth=1):
        self.image = image  # Either color, or image name
        self.ontop = []  # This is needs to be a list, and represents layers
        self.overlay = None  # Use the overlayer func, adds transparent colors

        self.drawOutline = drawOutline
        self.outlineColor = outlineColor
        self.outlineWidth = outlineWidth

    def blit(self, x, y):
        # Pixels on screen coordinates
        px = x * Map.m.tileSize[0] + Map.m.margin[0]
        py = y * Map.m.tileSize[1] + Map.m.margin[1]

        if type(self.image) is tuple:  # If it's a color
            pygame.draw.rect(self.window, self.image, (px, py, Map.m.tileSize[0], Map.m.tileSize[1]))
        elif type(self.image) is str:  # If it's an image
            self.window.blit(self.texture(self.image), (px, py))

        # Draws all the layers
        for image in self.ontop:
            self.window.blit(self.texture(image), (px, py))

        # Draws the transparent overlay
        if self.overlay is not None:
            self.window.blit(self.overlay, (px, py))

        if self.drawOutline:
            pygame.draw.rect(self.window, self.outlineColor, (px, py, Map.m.tileSize[0], Map.m.tileSize[1]),
                             self.outlineWidth)

    def overlayer(self, color, alpha, skip=False):
        # The skip parameter is for rescaling purposes
        self.overlay = pygame.Surface((Map.m.tileSize[0], Map.m.tileSize[1]), pygame.SRCALPHA, 32)
        self.overlay.fill(color + (alpha,))
        if not skip:
            self.overlayList.append(self)
            self.color = color
            self.alpha = alpha

    def rescale(self):
        self.texture.rescale()

        for ele in self.overlayList:
            # Recalls the overlay function, to reset the scale
            if ele.overlay is not None:
                ele.overlayer(ele.color, ele.alpha, skip=True)

    def getGridMouse(self):
        mouse = pygame.mouse.get_pos()
        # We "remove" the margin
        nx, ny = mouse[0]-Map.m.margin[0], mouse[1]-Map.m.margin[1]
        # Tests whether or not the mouse is within the grid
        if 0 <= nx < Map.m.tileSize[0] * Map.m.gridSize[0] and 0 <= ny < Map.m.tileSize[1] * Map.m.gridSize[1]:
            return Map.m.grid.get(math.trunc(nx / Map.m.tileSize[0]), math.trunc(ny / Map.m.tileSize[1]))
