import pygame
from settings import *
from textures import Texture
import time


def update_all(group, mouse):
    Message.update()
    Scroll.update(group)
    Button.update(group, mouse)
    Display.update(group, mouse)
    Input.update(group, mouse)
    Slider.update(group, mouse)


class Message:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)

    maxChars = 30  # This should be tied with width
    x, y = 0, WINDOW[1]-62
    w, h = 400, 32
    distance = 32  # How much each new message moves upwards
    textMargin = 10  # Left margin for text

    # This is for the transparent background
    background = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    background.fill(T_BLACK)  # format: (r, g, b, a)

    manager = []  # Keeps track of all messages

    def __init__(self, text, duration=4, color="RED", limiter=True):
        self.text = str(text)
        self.duration = duration  # Duration in seconds
        self.initialTime = time.time()
        self.color = COLORS[color]

        # If the char length is too long, create a new message with the rest
        if len(self.text) > self.maxChars:
            Message(self.text[self.maxChars::], self.duration)
            self.text = self.text[:self.maxChars]
            self.manager.append(self)

        else:
            self.manager.insert(0, self)  # Puts the newest message at the bottom

    @staticmethod
    def update():
        # We remove at the end
        remove = None
        for i, ele in enumerate(Message.manager):
            if time.time() - ele.initialTime > ele.duration:
                remove = ele

            Message.window.blit(Message.background, (Message.x, Message.y-(Message.distance*i)))
            ele.__text(i)

        if remove is not None:
            Message.manager.remove(remove)

    def __text(self, i):
        txt = self.font.render(self.text, True, self.color)
        self.window.blit(txt, pygame.Rect(self.x+self.textMargin, self.y-(self.distance*i), self.w, self.h))


class Button:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    manager = {}  # Keeps track of all the buttons, required for drawing, and updating them
    hovered = False

    def __init__(self, rect, func, string, group,
                 color="LIGHTERGREY", hover="LIGHTGREY", stringColor="BLACK",
                 outline=3, outline_color="BLACK", click="GREY", hidden=False):
        self.rect = pygame.Rect(rect)
        self.color = color  # Default color
        self.hover = hover  # Mouse hover color
        self.func = func  # What func to run when clicked
        self.group = group
        self.string = str(string)  # Text in button
        self.stringColor = stringColor  # Text color
        self.outline = outline  # Outline width
        self.outline_color = COLORS[outline_color]  # Duh
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

    @staticmethod
    def update(group, mouse):
        if group in Button.manager:
            Button.hovered = False
            for ele in Button.manager[group]:
                if not ele.hidden:
                    pygame.draw.rect(Button.window, ele.outline_color, ele.rect, ele.outline)  # Draws outline

                    if ele.rect.collidepoint(mouse):  # Mouse is hovering over a button
                        Button.hovered = True
                        Button.window.blit(Texture(ele.hover, ))
                        pygame.draw.rect(Button.window, ele.hover, ele.rect)

                        if pygame.mouse.get_pressed()[0] and ele.clicked is False:  # First time clicking
                            ele.run()

                        ele.hovering = True

                    else:  # If the mouse isn't hovering over anything
                        pygame.draw.rect(Button.window, ele.color, ele.rect)
                        ele.hovering = False
                        ele.clicked = False

                    if ele.clicked is True:  # The button is being clicked
                        pygame.draw.rect(Button.window, ele.click, ele.rect)

                    if not pygame.mouse.get_pressed()[0]:
                        ele.clicked = False

                    ele.__text()

    def __text(self):
        txt = self.font.render(self.string, True, self.stringColor)
        text_rect = txt.get_rect(center=(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3]/2))
        self.window.blit(txt, text_rect)

    def run(self):
        self.returned = self.func()
        self.clicked = True

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def kill(self):
        self.manager[self.group].remove(self)

    @staticmethod
    def killall(group):
        Button.manager[group] = []


class Overlay:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)

    def __init__(self, rect, group, exitButton=40):
        self.rect = pygame.Rect(rect)
        self.group = group
        self.message = Message("", 0)

        self.exitButton = exitButton  # Either 40 or False
        if not exitButton:
            self.button = Button((0, 0, 0, 0), None, "", self.group, hidden=True)
        else:
            self.button = Button((self.rect[0] + self.rect[2] - 40, self.rect[1], exitButton, 30), self.quit, "X",
                                 self.group)

        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

    def loop(self):
        self.running = True

        while self.running:
            pygame.draw.rect(self.window, "WHITE", self.rect)
            pygame.draw.rect(self.window, "BLACK", self.rect, 2)

            self.text(self.group, pygame.Rect(self.rect[0], self.rect[1]+5, self.rect[2]-self.exitButton, 30))

            # Draws all buttons
            Scroll.update(self.group)
            Button.update(self.group, self.mouse)
            Display.update(self.group, self.mouse)
            Input.update(self.group, self.mouse)
            Message.update()

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
            Scroll.events(event, self.group, self.mouse)

    def text(self, string, rect):
        txt = self.font.render(string, True, "BLACK")
        text_rect = txt.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
        self.window.blit(txt, text_rect)

    def quit(self):
        self.running = False
        Button.killall(self.group)
        Display.killall(self.group)
        Input.killall(self.group)
        return True


class Display:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    message = Message("", 0)
    manager = {}
    texture = Texture()
    hovered = False

    def __init__(self, rect, group, text=None, image=None, func=None, align="l", outline=3,
                 color="LIGHTERGREY", oColor="BLACK"):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.align = align # Can either align "l" for left, or "mid" for middle
        self.image = image
        self.group = group
        self.func = func
        self.returned = None
        self.hidden = False
        self.color = color

        self.outline = outline
        self.oColor = oColor

        # If a group exists, append it, else create it
        if group in self.manager:
            self.manager[group].append(self)
        else:
            self.manager[group] = [self]

    def __call__(self):
        return self.returned

    @staticmethod
    def update(group, mouse):
        if group in Display.manager:
            Display.hovered = False
            for box in Display.manager[group]:
                if not box.hidden:
                    pygame.draw.rect(Display.window, box.oColor, box.rect, box.outline)  # Outline
                    pygame.draw.rect(Display.window, box.color, box.rect)
                    if box.image is not None:
                        Display.window.blit(Display.texture(box.image, (box.rect[2], box.rect[3])), (box.rect[0], box.rect[1]))
                    if box.text is not None:
                        box.__text()
                    if box.rect.collidepoint(mouse):
                        Display.hovered = True
                        if box.func is not None and pygame.mouse.get_pressed()[0]:
                            box.returned = box.func()

    def __text(self):
        if self.align == "m":
            txt = self.font.render(self.text, True, "BLACK")
            text_rect = txt.get_rect(center=(self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2))
            self.window.blit(txt, text_rect)
        elif self.align == "l":
            txt = self.font.render(self.text, True, "BLACK")
            self.window.blit(txt, self.rect)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def kill(self):
        self.manager[self.group].remove(self)

    @staticmethod
    def killall(group):
        Display.manager[group] = []


class Input:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    message = Message("", 0)
    manager = {}

    def __init__(self, rect, text, group, onetime=False, outline=3, keep=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.group = group
        self.onetime = onetime  # If this is enabled, deletes the inputbox after
        self.outline = outline
        self.keep = keep  # If True keeps string when you want to type
        self.hidden = False

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
            pygame.draw.rect(self.window, "BLACK", self.rect, self.outline)  # Outline
            pygame.draw.rect(self.window, "GREY", self.rect)
            self.__text(inputString)
            self.message.update()
            pygame.display.update()

            pressed = self.__get_key()
            if pressed is not None:
                if pressed == pygame.K_BACKSPACE:
                    inputString = inputString[0:-1]
                # Ugly as all hell, but oh well
                elif pressed == pygame.K_RETURN or pressed == pygame.K_KP_ENTER or pressed == pygame.K_ESCAPE:
                    self.running = False
                elif 31 < pressed < 127:  # Letters, numbers, and special characters
                    inputString += chr(pressed)
                elif 255 < pressed < 266:  # Numpad numbers
                    inputString += chr(pressed - 208)

        self.running = True

        if self.onetime:
            self.manager[self.group].remove(self)

        self.inputString = inputString
        return self.inputString

    @staticmethod
    def update(group, mouse):
        if group in Input.manager:
            clicked = None  # So it draws them all before going into the one you clicked on
            for box in Input.manager[group]:
                if not box.hidden:
                    pygame.draw.rect(Input.window, "BLACK", box.rect, box.outline)  # Outline
                    pygame.draw.rect(Input.window, "LIGHTERGREY", box.rect)
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

    def __text(self, string):
        txt = self.font.render(self.text + str(string), True, "BLACK")
        self.window.blit(txt, self.rect)

    def changeText(self, new):
        self.inputString = str(new)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def kill(self):
        self.manager[self.group].remove(self)

    @staticmethod
    def killall(group):
        Input.manager[group] = []


class Scroll:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    manager = {}

    def __init__(self, rect, elements, group, movespeed=32, margin=10):
        self.rect = pygame.Rect(rect)
        self.elements = []
        self.group = group
        self.movespeed = movespeed
        self.margin = margin

        displace = 0
        # We're dealing with a list of lists
        for line in elements:
            for obj in line:
                obj.rect.y = self.rect.y + displace + margin
                obj.rect.x += self.rect.x + margin
                obj.group = self.group
                obj.hide()
            displace += obj.rect.height
            self.elements.append(line)

        self.manager[self.group] = self

    @staticmethod
    def update(group):
        if group in Scroll.manager:
            current = Scroll.manager[group]
            pygame.draw.rect(Scroll.window, "WHITE", current.rect)
            pygame.draw.rect(Scroll.window, "BLACK", current.rect, 2)

            for line in current.elements:
                for obj in line:
                    if current.rect.y <= obj.rect.y < current.rect.y + current.rect.height - obj.rect.height:
                        obj.show()
                    else:
                        obj.hide()

    @staticmethod
    def events(event, group, mouse):
        if Scroll.manager[group].rect.collidepoint(mouse):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if Scroll.manager[group].elements[0][0].rect.y <= Scroll.manager[group].rect.y:
                        Scroll.manager[group].move(Scroll.manager[group].movespeed)
                elif event.button == 5:
                    Scroll.manager[group].move(-Scroll.manager[group].movespeed)

    def move(self, amount):
        current = self.manager[self.group]
        for ui in current.elements:
            for thing in ui:
                thing.rect.y += amount


class Slider:
    pygame.init()
    window = pygame.display.set_mode((1, 1))  # This is suboptimal, but it works
    font = pygame.font.SysFont(FONT, 28)
    manager = {}

    def __init__(self, rect, elements, group, outline=3, pull_size=(15, 25), pull_outline=3,
                 outline_color="BLACK", color="LIGHTERGREY", pull_color="LIGHTGREY", pull_outline_color="BLACK"):
        self.rect = pygame.Rect(rect)
        self.elements = elements
        self.group = group
        self.x = 0

        self.ratio = rect[3] // len(elements)
        self.pull_size = pull_size
        self.pull = pygame.Rect(rect[0]+10, rect[1]+(rect[3]//2 - pull_size[1]//2), pull_size[0], pull_size[1])

        self.outline = outline
        self.outline_color = outline_color
        self.color = color
        self.pull_color = pull_color
        self.pull_outline = pull_outline
        self.pull_outline_color = pull_outline_color

        # If a group exists, append it, else create it
        if group in self.manager:
            self.manager[group].append(self)
        else:
            self.manager[group] = [self]

    def __call__(self):
        return self.elements[self.x]

    @staticmethod
    def update(group, mouse):
        if group in Slider.manager:
            for slide in Slider.manager[group]:
                pygame.draw.rect(Slider.window, slide.outline_color, slide.rect, slide.outline)  # Outline
                pygame.draw.rect(Slider.window, slide.color, slide.rect)
                pygame.draw.line(Slider.window, COLORS["BLACK"], (slide.rect[0]+10, slide.rect[1]+slide.rect[3]/2),
                                 (slide.rect[0]+slide.rect[2]-10, slide.rect[1]+slide.rect[3]/2), 1)
                pygame.draw.rect(Slider.window, slide.pull_outline_color, slide.pull, slide.pull_outline)
                pygame.draw.rect(Slider.window, slide.pull_color, slide.pull)


