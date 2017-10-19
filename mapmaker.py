import pygame
from tiles import *
import matrix
from settings import *
import copy
from prefabs import *
from maps import *
from ui import *


class Maker:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)
        self.group = "maker"
        self.sList = ["error_alpha.png", "error_alpha.png", "error_alpha.png", "error_alpha.png", "error_alpha.png"]
        self.sCurrent = 0
        self.secondaryTexture = BLACK
        self.selection = None
        self.page = 0
        self.thumbnailSize = 32
        self.currentLayer = 0
        self.map = Map([15, 12], "first")

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
            self.displayBox.update(self.group, self.mouse)
            self.inputBox.update(self.group, self.mouse)
            self.error.update()

            self.events()

            pygame.display.update()

    def events(self):
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()
        self.selection = self.tile.getGridMouse()

        # Massive try because inputs aren't all connected to the cursor location
        # So if I put <if self.selection is None> you wouldn't be able to move, etc...
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.prefab.o_quit()
                # Checks if the mouse isn't on a button or display box
                if not (Button.hovered or Display.hovered):
                    # TAB
                    if self.pressed[pygame.K_TAB]: self.prefab.o_textureSelect()
                    # O
                    elif self.pressed[pygame.K_o]: self.selection.drawOutline = False
                    # I
                    elif self.pressed[pygame.K_i]: self.selection.drawOutline = True
                    # SPACE + CLICK
                    elif self.pressed[pygame.K_SPACE]:
                        if pygame.mouse.get_pressed()[0]: self.move()
                        else: self.mouseMove = 0
                    # LEFT CLICK
                    elif pygame.mouse.get_pressed()[0]:
                        # LEFT CLICK + SHIFT
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            if self.currentLayer < len(self.tile.image) - 1:
                                self.selection.image[self.currentLayer+1] = self.sList[self.sCurrent]
                        # LEFT CLICK + CTRL
                        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                            if type(self.selection.image[self.currentLayer]) is str:
                                self.sList[self.sCurrent] = self.selection.image[self.currentLayer]
                                self.resetDisplay()
                        # LEFT CLICK
                        else: self.selection.image[self.currentLayer] = self.sList[self.sCurrent]
                    # RIGHT CLICK
                    elif pygame.mouse.get_pressed()[2]:
                        # RIGHT CLICK + SHIFT
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.selection.image = [None, None, None, None, None, None]
                        # RIGHT CLICK
                        else: self.selection.image[self.currentLayer] = None
                    # Keep this one at bottom, so the space+click doesn't interfere with the rest
                    # SCROLL
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # SCROLL + SHIFT
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            # UP SCROLL + SHIFT
                            if event.button == 4: self.currentLayer = self.check(self.currentLayer, self.tile.image, 1)
                            # DOWN SCROLL + SHIFT
                            if event.button == 5: self.currentLayer = self.check(self.currentLayer, 0, 0)
                        # SCROLL + CTRL
                        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                            if event.button == 4: self.sCurrent = self.check(self.sCurrent, self.sList, 1)
                            if event.button == 5: self.sCurrent = self.check(self.sCurrent, 0, 0)

                        else:
                            if event.button == 4:
                                Map.m.tileSize[0] += 5
                                Map.m.tileSize[1] += 5
                                self.tile.rescale()
                            if event.button == 5:
                                Map.m.tileSize[0] -= 5
                                Map.m.tileSize[1] -= 5
                                self.tile.rescale()

        except AttributeError:
            Error("Cursor outside of grid", duration=1)

    def check(self, a, b, c):
        # Keeps a within 0 and len(b), when you add/subtract
        if c:
            if a < len(b) - 1:
                a += 1
        else:
            if a > 0:
                a -= 1
        self.resetDisplay()
        return a

    def move(self):
        if not self.mouseMove:
            self.mouseMove = self.mouse
            self.originalMargin = copy.copy(Map.m.margin)
        Map.m.margin[0] = self.mouse[0] - self.mouseMove[0] + self.originalMargin[0]
        Map.m.margin[1] = self.mouse[1] - self.mouseMove[1] + self.originalMargin[1]

    def defaultUI(self):
        b = WINDOW[1] - 30
        self.button = Button((WINDOW[0] - 40, 0, 40, 30), self.prefab.o_quit, "X", self.group)
        Button((0, 0, 80, 30), self.prefab.o_newgrid, "New", self.group)
        Button((80, 0, 80, 30), self.prefab.o_loadmap, "Load", self.group)
        Button((160, 0, 160, 30), self.prefab.o_textureSelect, "Textures", self.group)
        Button((320, 0, 160, 30), self.prefab.o_settings, "Settings", self.group)
        Display((0, b, 240, 30), self.group, text="Map: "+Map.m.name)
        Display((240, b, 320, 30), self.group, text="Texture: "+self.sList[self.sCurrent])
        for i in range(5):
            if i == self.sCurrent:
                Display((560+i*30, b, 30, 30), self.group, func=partial(self.selected, i),
                        image=self.sList[i], outline=5, oColor=RED)
            else:
                Display((560+i*30, b, 30, 30), self.group, func=partial(self.selected, i), image=self.sList[i])

        Display((WINDOW[0]-110, b, 80, 30), self.group, text="Layer", align="m")
        for i in range(6):
            if i == self.currentLayer:
                Display((WINDOW[0]-30,b-i*30,30,30), self.group, str(i), func=partial(self.layer, i),
                        color=DARKGREY, align="m")
            else:
                Display((WINDOW[0]-30,b-i*30,30,30), self.group, str(i), func=partial(self.layer, i),
                        color=GREY, align="m")

    def resetDisplay(self):
        self.button.killall(self.group)
        self.inputBox.killall(self.group)
        self.displayBox.killall(self.group)
        self.defaultUI()

    def layer(self, number):
        self.currentLayer = number
        self.resetDisplay()

    def selected(self, number):
        self.sCurrent = number
        self.resetDisplay()

    def quit(self):
        self.running = False


m = Maker()
