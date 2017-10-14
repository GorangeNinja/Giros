import pygame
from settings import *
from textures import Texture
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

    # This is for the transparent background
    background = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    background.fill(T_BLACK)  # format: (r, g, b, a)

    manager = []  # Keeps track of all error messages

    def __init__(self, text, duration=4, color=RED, limiter=True):
        self.text = str(text)
        self.duration = duration  # Duration in seconds
        self.initialTime = time.time()
        self.color = color
        self.limiter = limiter  # TODO If the message already exists do not make it

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
        txt = self.font.render(self.text, True, self.color)
        self.window.blit(txt, pygame.Rect(self.x+self.textMargin, self.y-(self.distance*i), self.w, self.h))


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


class Overlay:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)

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

        self.inputBox = Input((0, 0, 0, 0), "", self.group)
        self.displayBox = Display((0, 0, 0, 0), self.group)
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

    def loop(self):
        self.running = True

        while self.running:
            pygame.draw.rect(self.window, WHITE, self.rect)
            pygame.draw.rect(self.window, BLACK, self.rect, 2)

            self.text(self.group, pygame.Rect(self.rect[0], self.rect[1]+5, self.rect[2]-self.exitButton, 30))

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
        for event in pygame.event.get():
            if self.exitButton:
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.quit()

    def text(self, string, rect):
        txt = self.font.render(string, True, BLACK)
        text_rect = txt.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
        self.window.blit(txt, text_rect)

    def quit(self):
        self.running = False
        return True


class Display:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    error = Error("", 0)
    manager = {}
    texture = Texture()

    def __init__(self, rect, group, text=None, image=None, func=None, align="l", outline=3):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.align = align # Can either align "l" for left, or "mid" for middle
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


class Input:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    error = Error("", 0)
    manager = {}

    def __init__(self, rect, text, group, onetime=False, outline=3, keep=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.group = group
        self.onetime = onetime  # If this is enabled, deletes the inputbox after
        self.outline = outline
        self.keep = keep  # If True keeps string when you want to type

        self.inputString = ""

        # If a group exists, append it, else create it
        if group in self.manager:
            self.manager[group].append(self)
        else:
            self.manager[group] = [self]

        self.running = True

    # Only returns strings
    def __call__(self):
        return self.inputString

    # Tries to return int
    def intCall(self):
        try:
            return int(self.inputString)
        except:
            return None

    def run(self):
        self.update(self.group, None)  # So it draws all the boxes, before going into typing mode

        if self.keep: inputString = self.inputString
        else: inputString = ""

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
                # Ugly as all hell, but oh well
                elif pressed == pygame.K_RETURN or pressed == pygame.K_KP_ENTER:
                    self.running = False
                elif pressed == pygame.K_ESCAPE:
                    self.running = False
                    inputString = None
                elif 31 < pressed < 127:  # Letters, numbers, and special characters
                    inputString += chr(pressed)
                elif 255 < pressed < 266:  # Numpad numbers
                    inputString += chr(pressed - 208)

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
        # Infinite loop until a key/mouse is pressed
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
        self.inputString = str(new)

    def kill(self):
        self.manager[self.group].remove(self)

    def killall(self, group):
        self.manager[group] = []
