import pygame
from buttons import *
from tiles import *
import matrix
from settings import *
import copy
from inputbox import *
from displaybox import *
import overlays
from errors import *
from prefabs import *
from maps import *


class Loop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)
        self.group = "maker"
        self.selectedTexture = "error_alpha.png"
        self.secondaryTexture = BLACK
        self.selection = None

        self.map = Map([20, 14], "first", [32, 32], [50, 50])
        self.tile = Tile(None)
        self.tile.texture.bulk()
        self.error = Error("", 0)
        self.prefab = Prefab(self)
        self.inputBox = Input((0, 0, 0, 0), "", self.group)
        self.displayBox = Display((0, 0, 0, 0), self.group)

        self.defaultUI()

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()
        self.mouseMove = 0  # Used in getting the amount the mouse moved
        self.originalMargin = Map.m.margin  # Keeps the original margin so it knows how much to move

        self.running = True
        self.loop()


    def loop(self):
        while self.running:
            self.window.fill(BLACK)
            # Draws all tiles
            for ele in Map.m.grid.all():
                ele[2].blit(ele[0], ele[1])

            # Draws all buttons
            self.button.update(self.group, self.mouse)
            self.displayBox.update(self.group)
            self.inputBox.update(self.group, self.mouse)
            self.error.update()

            self.events()

            pygame.display.update()

    def events(self):
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()
        self.selection = self.tile.getGridMouse()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.prefab.o_quit()

            elif self.pressed[pygame.K_TAB]: self.prefab.o_textureSelect()
            elif self.pressed[pygame.K_o]: self.selection.drawOutline = False
            elif self.pressed[pygame.K_i]: self.selection.drawOutline = True

            elif self.pressed[pygame.K_SPACE]:
                if pygame.mouse.get_pressed()[0]:
                    self.move()
                else:
                    self.mouseMove = 0

            # Keep this one at bottom, so the space+click doesn't interfere with the rest
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        if self.selection.ontop is None: self.selection.ontop = []
                        self.selection.ontop.append(self.selectedTexture)
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if type(self.selection.image) is str:
                            self.selectedTexture = self.selection.image
                            self.resetDisplay()
                    else:
                        self.selection.image = self.selectedTexture
                if event.button == 3:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.selection.ontop = []
                    else:
                        self.selection.image = self.secondaryTexture
                if event.button == 4:
                    Map.m.tileSize[0] += 5
                    Map.m.tileSize[1] += 5
                    self.tile.rescale()
                if event.button == 5:
                    Map.m.tileSize[0] -= 5
                    Map.m.tileSize[1] -= 5
                    self.tile.rescale()

    def showGrid(self):
        for ele in Map.m.grid.all():
            ele[2].drawOutline = not ele[2].drawOutline

    def move(self):
        if not self.mouseMove:
            self.mouseMove = self.mouse
            self.originalMargin = copy.copy(Map.m.margin)
        Map.m.margin[0] = self.mouse[0] - self.mouseMove[0] + self.originalMargin[0]
        Map.m.margin[1] = self.mouse[1] - self.mouseMove[1] + self.originalMargin[1]

    def defaultUI(self):
        self.button = Button((WINDOW[0] - 40, 0, 40, 30), self.prefab.o_quit, "X", self.group)
        self.b_new = Button((0, 0, 80, 30), self.prefab.o_newgrid, "New", self.group)
        self.b_load = Button((80, 0, 80, 30), self.prefab.o_loadmap, "Load", self.group)
        self.b_texture = Button((160, 0, 160, 30), self.prefab.o_textureSelect, "Textures", self.group)
        self.d_currentMap = Display((0, WINDOW[1]-30, 240, 30), self.group, text="Map: "+Map.m.name)
        self.d_currentTexture = Display((240, WINDOW[1]-30, 320, 30), self.group, text="Texture: "+self.selectedTexture)
        self.d_currentTextureThumbnail = Display((560, WINDOW[1] - 30, 30, 30), self.group, image=self.selectedTexture)

    def resetDisplay(self):
        self.button.killall(self.group)
        self.inputBox.killall(self.group)
        self.displayBox.killall(self.group)
        self.defaultUI()

    def quit(self):
        self.running = False


l = Loop()
