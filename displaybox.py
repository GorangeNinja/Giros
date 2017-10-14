import pygame
from settings import *
from errors import *
import textures


class Display:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    error = Error("", 0)
    manager = {}
    texture = textures.Texture()

    def __init__(self, rect, group, text=None, image=None, func=None, align="l", outline=3):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.align = align # Can eigher align "l" for left, or "mid" for middle
        self.image = image
        self.group = group
        self.func = func
        self.returned = None

        self.outline = outline

        if image is not None:
            if image not in self.texture.custom:
                self.texture.addCustom(image, rect[2], rect[3])

        # If a group exists, append it, else create it
        if group in self.manager:
            self.manager[group].append(self)
        else:
            self.manager[group] = [self]

    def __call__(self):
        return self.returned

    def update(self, group, mouse):
        for box in self.manager[group]:
            pygame.draw.rect(self.window, BLACK, box.rect, box.outline)  # Outline
            pygame.draw.rect(self.window, LIGHTERGREY, box.rect)
            if box.image is not None:
                self.window.blit(self.texture.callCustom(box.image), (box.rect[0], box.rect[1]))
            if box.text is not None:
                box.__text()
            if box.func is not None:
                if box.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    box.returned = box.func()


    def __text(self):
        if self.align == "mid":
            txt = self.font.render(self.text, True, BLACK)
            text_rect = txt.get_rect(center=(self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2))
            self.window.blit(txt, text_rect)
        elif self.align == "l":
            txt = self.font.render(self.text, True, BLACK)
            self.window.blit(txt, self.rect)


    def kill(self):
        self.manager[self.group].remove(self)

    def killall(self, group):
        self.manager[group] = []
