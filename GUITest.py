from ui import *
import pygame
from settings import *


class Tester:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)
        self.clock = pygame.time.Clock()
        self.group = "maker"

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        self.initUI()

        self.running = True
        self.loop()

    def initUI(self):
        Button((0, 0, 40, 40), self.quit, "X", self.group)

        l = []
        for i in range(40):
            l.append([Button((0, 0, 180, 32), self.quit, "testa{}".format(i), self.group)])
        Scroll((100, 100, 200, 500), l, self.group)

        Slider((400, 400, 400, 35), [10, 25, 33], self.group)

    def loop(self):
        while self.running:
            self.window.fill(BROWN)

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


    def quit(self):
        self.running = False


t = Tester()
