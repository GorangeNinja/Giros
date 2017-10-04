import pygame
from settings import *
from buttons import *
import inputbox
from errors import *


class Overlay:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont('Times New Roman', 28)

    def __init__(self, rect, group, exitButton=40):
        self.rect = pygame.Rect(rect)
        self.group = group
        self.error = Error("", 0)

        self.exitButton = exitButton  # Either 40 or False
        if not exitButton:
            self.button = Button((0, 0, 0, 0), None, "", self.group, hidden=True)
        else:
            self.button = Button((self.rect[0] + self.rect[2] - 40, self.rect[1], exitButton, 30), self.quit, "X",
                                 self.group)

        self.inputBox = inputbox.Input((0, 0, 0, 0), "", self.group)
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

    def loop(self):
        self.running = True

        while self.running:
            pygame.draw.rect(self.window, WHITE, self.rect)
            pygame.draw.rect(self.window, BLACK, self.rect, 2)

            self.text(self.group, pygame.Rect(self.rect[0], self.rect[1], self.rect[2]-self.exitButton, 30))

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
                pygame.quit()

    def text(self, string, rect):
        txt = self.font.render(string, True, BLACK)
        text_rect = txt.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
        self.window.blit(txt, text_rect)

    def quit(self):
        self.running = False

    def varQuit(self):
        self.running = False
        return True