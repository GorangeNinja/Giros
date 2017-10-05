import pygame
from settings import *
import time


class Error:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont('Times New Roman', 28)
    maxChars = 20

    x, y = 0, WINDOW[1]-62
    w, h = 290, 32
    distance = 32
    textMargin = 10

    background = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    background.fill(T_BLACK)

    manager = []

    def __init__(self, text, duration=4):
        self.text = str(text)
        self.duration = duration
        self.initialTime = time.time()

        if len(self.text) > self.maxChars:
            Error(self.text[self.maxChars::])
            self.text = self.text[:self.maxChars]

        self.manager.append(self)

    def update(self):
        remove = None
        for i, ele in enumerate(self.manager):
            if time.time() - ele.initialTime > ele.duration:
                remove = ele

            self.window.blit(self.background, (self.x, self.y-(self.distance*i)))
            ele.__text(i)

        if remove is not None: self.manager.remove(remove)

    def __text(self, i):
        txt = self.font.render(self.text, True, RED)
        self.window.blit(txt, pygame.Rect(self.textMargin, self.y-(self.distance*i), self.w, self.h))
