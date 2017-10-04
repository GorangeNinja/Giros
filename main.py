import pygame
import matrix
from tiles import *
import buttons
from settings import *


class Loop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)

        self.tile = Tile(None)
        self.grid = matrix.Grid(GRIDSIZE, fill=Tile("textures_00.png"))

        self.bgroup = "main"

        self.Button = buttons.Button((0, 0, 80, 30), None, "File", self.bgroup)
        self.b2 = buttons.Button((80, 0, 80, 30), self.draw, "Draw", self.bgroup)
        self.b3 = buttons.Button((160, 0, 120, 30), self.overlay, "Overlay", self.bgroup)
        self.b4 = buttons.Button((280, 0, 80, 30), self.star, "Star", self.bgroup)
        self.b5 = buttons.Button((360, 0, 120, 30), self.tile.rescale, "Rescale", self.bgroup)
        self.b6 = buttons.Button((480, 0, 80, 30), self.clear, "Clear", self.bgroup)
        self.b7 = buttons.Button((560, 0, 80, 30), self.night, "Night", self.bgroup)
        self.b8 = buttons.Button((640, 0, 80, 30), self.show, "Show", self.bgroup)
        self.bquit = buttons.Button((WINDOW[0]-40, 0, 40, 30), self.quit, "X", self.bgroup)

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        self.running = True
        self.loop()


    def loop(self):
        while self.running:
            self.window.fill(BLACK)
            # Draws all tiles
            for ele in self.grid.all():
                ele[2].blit(ele[0], ele[1])

            # Draws all buttons
            self.Button.update(self.bgroup, self.mouse)

            self.events()

            pygame.display.update()

    def events(self):
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MARGIN[0] -= 25
                if event.key == pygame.K_RIGHT:
                    MARGIN[0] += 25
                if event.key == pygame.K_UP:
                    MARGIN[1] -= 25
                if event.key == pygame.K_DOWN:
                    MARGIN[1] += 25
                if event.key == pygame.K_x:
                    TILESIZE[0] += 5
                    TILESIZE[1] += 5
                    self.tile.rescale()
                if event.key == pygame.K_z:
                    TILESIZE[0] -= 5
                    TILESIZE[1] -= 5
                    self.tile.rescale()
                if event.key == pygame.K_SPACE:
                    self.grid.put(*self.tile.getGridMouse(), Tile("textures_00.png", ["textures_24_alpha.png"]))


    def quit(self):
        self.running = False

    def draw(self):
        self.grid.fill(self.grid.rect(10, 10, 4, 4),
                       Tile("textures_00.png", ["textures_35_alpha.png", "textures_24_alpha.png"], outlineWidth=1))

    def clear(self):
        self.grid.fill(self.grid.all(), Tile(BLACK))

    def star(self):
        for ele in self.grid.star(0, 5, 5):
            ele[2].overlayer(RED, 25)

    def overlay(self):
        self.grid.get(5, 5).overlayer(RED, 100)

    def quit(self):
        self.running = False

    def night(self):
        for ele in self.grid.all():
            ele[2].overlayer(BLACK, 200)

    def show(self):
        print(self.grid)

l = Loop()