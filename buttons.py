import pygame
from settings import *


class Button:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    manager = {}  # Keeps track of all the buttons, required for drawing, and updating them

    def __init__(self, rect, func, string, group, color=LIGHTERGREY, hover=LIGHTGREY,
                stringColor=BLACK, outline=3, outline_color=BLACK, click=GREY, hidden=False):
        self.rect = pygame.Rect(rect)
        self.color = color  # Default color
        self.hover = hover  # Mouse hover color
        self.func = func  # What func to run when clicked
        self.group = group
        self.string = str(string)  # Text in button
        self.stringColor = stringColor  # Text color
        self.outline = outline  # Outline width
        self.outline_color = outline_color  # Duh
        self.click = click  # Click color
        self.hidden = hidden  # Bool

        self.returned = None  # What's returned when launching the function
        self.clicked = False  # To stop hold down spam click from happening
        self.hovering = False

        if group in self.manager:
            self.manager[group].append(self)
        else: self.manager[group] = [self]

    def __call__(self):
        return self.returned

    def update(self, group, mouse):
        for ele in self.manager[group]:
            if not ele.hidden:
                pygame.draw.rect(self.window, ele.outline_color, ele.rect, ele.outline)  # Draws outline

                if ele.rect.collidepoint(mouse):  # Mouse is hovering over a button
                    pygame.draw.rect(self.window, ele.hover, ele.rect)

                    if pygame.mouse.get_pressed()[0] and ele.clicked is False:  # First time clicking
                        ele.returned = ele.func()
                        ele.clicked = True

                    ele.hovering = True

                else:  # If the mouse isn't hovering over anything
                    pygame.draw.rect(self.window, ele.color, ele.rect)
                    ele.hovering = False
                    ele.clicked = False

                if ele.clicked is True:  # The button is being clicked
                    pygame.draw.rect(self.window, ele.click, ele.rect)

                if not pygame.mouse.get_pressed()[0]:
                    ele.clicked = False

                ele.__text()

    def __text(self):
        txt = self.font.render(self.string, True, self.stringColor)
        text_rect = txt.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3]/2))
        self.window.blit(txt, text_rect)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def toggle(self):
        self.hidden = not self.hidden

    def kill(self):
        self.manager[self.group].remove(self)

    def killall(self, group):
        self.manager[group] = []
