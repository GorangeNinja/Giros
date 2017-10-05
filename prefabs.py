import pygame
from buttons import *
from tiles import *
import matrix
from settings import *
import inputbox
import overlays
from errors import *
from maps import *
from functools import partial


class Prefab:
    uniqueGroup = 0

    def __init__(self, parent):
        self.parent = parent

    def o_account(self):
        group = "Account"
        w, h, m = 300, 160, 10
        x, y = WINDOW[0]/2-w/2, WINDOW[1]/2-h/2
        overlay = overlays.Overlay((x, y, w, h), group)
        overlay.username = inputbox.Input((x+m, y+40, w-2*m, 32), "Username: ", group)
        overlay.password = inputbox.Input((x+m, y+72, w-2*m, 32), "Password: ", group)
        overlay.submit = Button((x+m, y+110, w-2*m, 40), overlay.quit, "Submit", group)
        overlay.loop()
        return overlay.username(), overlay.password()

    def o_newgrid(self):
        group = "New Grid"
        w, h, m = 400, 300, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = overlays.Overlay((x, y, w, h), group)
        overlay.width = inputbox.Input((x + m, y + 40, w - 2 * m, 32), "Width: ", group)
        overlay.height = inputbox.Input((x + m, y + 72, w - 2 * m, 32), "Height: ", group)
        overlay.name = inputbox.Input((x + m, y + 114, w - 2 * m, 32), "Name: ", group)
        overlay.fill = inputbox.Input((x + m, y + 156, w - 2 * m - 32, 32), "Fill: ", group)
        overlay.paste = Button((x + w - 32 - m, y + 156, 32, 32), partial(overlay.fill.changeText, self.parent.selectedTexture), "#", group)
        overlay.submit = Button((x + m, y + 250, w - 2 * m, 40), overlay.quit, "Create", group)
        overlay.loop()
        if overlay.submit():
            if type(overlay.width()) is int and type(overlay.height()) is int:
                if type(overlay.name()) is str:
                    self.parent.mapgroup = overlay.name()
                    if type(overlay.fill()) is str:
                        self.parent.map = Map([overlay.width(), overlay.height()], self.parent.mapgroup, [32, 32], [50, 50], fill=overlay.fill())
                    else:
                        self.parent.map = Map([overlay.width(), overlay.height()], self.parent.mapgroup, [32, 32], [50, 50])
                    self.parent.tile.rescale()
                    self.parent.resetDisplay()
                else:
                    Error("Excepted string name")
            else:
                Error("Expected integer width/height")

    def o_fill(self):
        group = "Fill"
        w, h, m = 400, 142, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = overlays.Overlay((x, y, w, h), group)
        overlay.fill = inputbox.Input((x + m, y + 40, w - 2 * m, 32), "Texture Name: ", group)
        overlay.submit = Button((x + m, y + 92, w - 2 * m, 40), overlay.quit, "Change", group)
        overlay.loop()
        return overlay.fill()

    def o_quit(self):
        group = "Quit"
        w, h, m = 400, 174, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = overlays.Overlay((x, y, w, h), group, exitButton=False)
        overlay.message = inputbox.Input((x + m, y + 40, w - 2 * m, 32), "All unsaved progress will be lost", group, clickable=False, outline=0)
        overlay.message2 = inputbox.Input((x + m, y + 72, w - 2 * m, 32), "Are you sure?", group, clickable=False, outline=0)
        overlay.no = Button((x + m, y + 122, 80, 40), overlay.quit, "No", group)
        overlay.yes = Button((x + w - m - 80, y + 122, 80, 40), overlay.quit, "Yes", group)
        overlay.loop()
        if overlay.yes(): self.parent.quit()

    def o_textureSelect(self):
        group = "Textures"
        w, h, m = WINDOW[0]-100, WINDOW[1]-100, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = overlays.Overlay((x, y, w, h), group)
        overlay.loop()

    def o_loadmap(self):
        group = "Load Map"
        w, h, m = 400, 172, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = overlays.Overlay((x, y, w, h), group)
        overlay.message = inputbox.Input((x + m, y + 40, w - 2 * m, 32), "Current map will NOT be lost", group, clickable=False, outline=0)
        overlay.name = inputbox.Input((x + m, y + 80, w - 2 * m, 32), "Name: ", group)
        overlay.submit = Button((x + m, y + 122, w - 2 * m, 40), overlay.quit, "Load", group)
        overlay.loop()
        if overlay.submit():
            if type(overlay.name()) is str:
                if overlay.name() in Map.manager:
                    self.parent.map.load(overlay.name())
                    self.parent.resetDisplay()
                else:
                    Error("Map doesn't exist")
            else:
                Error("Expected string")

    def __group(self):  # Overlays, buttons, and inputboxes expect an unique group string
        self.uniqueGroup += 1
        return str(self.uniqueGroup)
