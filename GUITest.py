from ui import *
import pygame
from settings import *
from textures import Texture
from functools import partial


class Tester:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1300, 900))
        self.clock = pygame.time.Clock()
        self.group = "maker"

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        Texture(0, 0, 0, 0).bulk("")

        self.initUI()

        self.running = True
        self.loop()

    def initUI(self):
        Button((0, 0, 40, 40), self.quit, "X", self.group, color=["s_spelunky"], stringColor="WHITE")
        Button((200, 150, 100, 100), self.over, "OVER!!", self.group, color=["s_ui"])

    def loop(self):
        while self.running:
            self.window.fill(COLORS["BROWN"])

            # Draws all buttons
            update_all(self.group, self.mouse)

            self.events()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.update()

    def events(self):
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            Scroll.events(event, self.group, self.mouse)

    def over(self):
        group = "tessss"
        o = Overlay((500, 100, 500, 500), group)
        l = []
        for i in range(15):
            l.append([Button((0, 0, 226, 50), self.nothing, "ad{}".format(i), group, color=["s_ui", 0],
                             hover=["s_ui", 1], click=["s_ui", 2], outline=-1)])
        l.append([Button((0, 0, 226, 50), partial(l[14][0].color.rescale, (150, 50)), "tester", group, color=["s_ui", 0],
                         hover=["s_ui", 1], click=["s_ui", 2], outline=-1)])
        Scroll((525, 100, 250, 520), l, group, movespeed=50, color=["s_hyptosis1", 4])
        o.loop()

    def nothing(self):
        pass

    def quit(self):
        self.running = False


t = Tester()
