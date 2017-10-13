import pygame
from settings import *
from errors import *


class Input:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    error = Error("", 0)
    manager = {}

    def __init__(self, rect, text, group, onetime=False, outline=3):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.group = group
        self.onetime = onetime  # If this is enabled, deletes the inputbox after
        self.outline = outline

        self.inputString = ""

        # If a group exists, append it, else create it
        if group in self.manager:
            self.manager[group].append(self)
        else: self.manager[group] = [self]

        self.running = True

    def __call__(self):
        return self.inputString

    def intCall(self):
        try:
            return int(self.inputString)
        except:
            return None

    def run(self):
        self.update(self.group, None)  # So it draws all the boxes, before going into typing mode
        inputString = ""
        while self.running:
            # We draw before input, cause when it's inside infinite wait loop we want everything drawn
            pygame.draw.rect(self.window, BLACK, self.rect, self.outline)  # Outline
            pygame.draw.rect(self.window, GREY, self.rect)
            self.__text(inputString)
            self.error.update()
            pygame.display.update()

            pressed = self.__get_key()
            if pressed is not None:
                if pressed == pygame.K_BACKSPACE:
                    inputString = inputString[0:-1]
                elif pressed == pygame.K_RETURN or pressed == pygame.K_KP_ENTER:
                    self.running = False
                elif pressed == pygame.K_ESCAPE:
                    self.running = False
                    inputString = None
                elif 31 < pressed < 127:  # Letters, numbers, and special characters
                    inputString += chr(pressed)
                elif 255 < pressed < 266:  # Numpad numbers
                    inputString += chr(pressed - 208)
                elif pressed == 269:
                    inputString += "_"

        self.running = True
        if self.onetime:
            self.manager[self.group].remove(self)

        self.inputString = inputString
        return self.inputString

    def update(self, group, mouse):
        clicked = None  # So it draws them all before going into the one you clicked on
        for box in self.manager[group]:
            pygame.draw.rect(self.window, BLACK, box.rect, box.outline)  # Outline
            pygame.draw.rect(self.window, LIGHTERGREY, box.rect)
            box.__text(box.inputString)

            if mouse is not None:
                if box.rect.collidepoint(mouse):
                    if pygame.mouse.get_pressed()[0]:
                        clicked = box

        if clicked is not None:
            clicked.run()

    def __get_key(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.running = False
                return
            else:
                pass

    def __text(self, string):
        txt = self.font.render(self.text + str(string), True, BLACK)
        self.window.blit(txt, self.rect)

    def changeText(self, new):
        self.inputString = new

    def kill(self):
        self.manager[self.group].remove(self)

    def killall(self, group):
        self.manager[group] = []
