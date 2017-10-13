import pygame
from settings import *
import time


class Error:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)

    maxChars = 30  # This should be tied with width
    x, y = 0, WINDOW[1]-62
    w, h = 400, 32
    distance = 32  # How much each new error message moves upwards
    textMargin = 10  # Left margin for text
    textColor = RED

    # This is for the transparent background
    background = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    background.fill(T_BLACK)  # format: (r, g, b, a)

    manager = []  # Keeps track of all error messages

    def __init__(self, text, duration=4):
        self.text = str(text)
        self.duration = duration  # Duration in seconds
        self.initialTime = time.time()

        # If the char length is too long, create a new error message with the rest
        if len(self.text) > self.maxChars:
            Error(self.text[self.maxChars::], self.duration)
            self.text = self.text[:self.maxChars]

        self.manager.insert(0, self)

    def update(self):
        # We remove at the end
        remove = None
        for i, ele in enumerate(self.manager):
            if time.time() - ele.initialTime > ele.duration:
                remove = ele

            self.window.blit(self.background, (self.x, self.y-(self.distance*i)))
            ele.__text(i)

        if remove is not None:
            self.manager.remove(remove)

    def __text(self, i):
        txt = self.font.render(self.text, True, self.textColor)
        self.window.blit(txt, pygame.Rect(self.x+self.textMargin, self.y-(self.distance*i), self.w, self.h))
