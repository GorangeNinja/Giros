import pygame
from buttons import *
from tiles import *
import matrix
from settings import *
import copy
import inputbox
import overlays
from errors import *
from prefabs import *
import maps


class Loop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)
        self.group = "maker"
        self.mapgroup = "first"

        self.map = maps.Map([20, 14], self.group, [32, 32], [50, 50])
        self.tile = Tile(None, self.mapgroup)
        self.tile.texture.bulk()
        self.error = Error("", 0)
        self.prefab = Prefab(self)

        self.defaultUI()

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()
        self.mouseMove = 0  # Used in getting the amount the mouse moved
        self.originalMargin = self.map.margin  # Keeps the original margin so it knows how much to move

        self.running = True
        self.loop()


    def loop(self):
        while self.running:
            self.window.fill(BLACK)
            # Draws all tiles
            for ele in self.map.grid.all():
                ele[2].blit(ele[0], ele[1])

            # Draws all buttons
            self.button.update(self.group, self.mouse)
            self.inputBox.update(self.group, self.mouse)
            self.error.update()

            self.events()

            pygame.display.update()

    def events(self):
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.pressed[pygame.K_SPACE]:
                if pygame.mouse.get_pressed()[0]:
                    self.move()
                else:
                    self.mouseMove = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.map.tileSize[0] += 5
                    self.map.tileSize[1] += 5
                    self.tile.rescale()
                if event.button == 5:
                    self.map.tileSize[0] -= 5
                    self.map.tileSize[1] -= 5
                    self.tile.rescale()

    def showGrid(self):
        for ele in self.map.grid.all():
            ele[2].drawOutline = not ele[2].drawOutline

    def move(self):
        if not self.mouseMove:
            self.mouseMove = self.mouse
            self.originalMargin = copy.copy(self.map.margin)
        self.map.margin[0] = self.mouse[0] - self.mouseMove[0] + self.originalMargin[0]
        self.map.margin[1] = self.mouse[1] - self.mouseMove[1] + self.originalMargin[1]

    def defaultUI(self):
        self.button = Button((WINDOW[0] - 40, 0, 40, 30), self.prefab.o_quit, "X", self.group)
        self.b_new = Button((0, 0, 80, 30), self.prefab.o_newgrid, "New", self.group)
        self.inputBox = inputbox.Input((0, 0, 0, 0), "", self.group)
        self.currentmap = inputbox.Input((80, 0, 160, 30), "Map: "+self.mapgroup, self.group, clickable=False)
        self.resetUI = Button((240, 0, 160, 30), self.resetUI, "Reset UI", self.group)

    def resetUI(self):
        self.button.killall()
        self.inputBox.killall()
        self.defaultUI()

    def quit(self):
        self.running = False


l = Loop()
