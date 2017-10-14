import pygame
from tiles import *
import matrix
from settings import *
from maps import *
from functools import partial
import textures
from ui import *


# This is where dreams come to die
class Prefab:
    uniqueGroup = 0
    texture = textures.Texture()

    def __init__(self, parent):
        self.parent = parent

    def o_newgrid(self):
        group = "New Grid"
        w, h, m = 400, 300, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group)
        width = Input((x + m, y + 40, w - 2 * m, 32), "Width: ", group)
        height = Input((x + m, y + 72, w - 2 * m, 32), "Height: ", group)
        name = Input((x + m, y + 114, w - 2 * m, 32), "Name: ", group)
        fill = Input((x + m, y + 156, w - 2 * m - 64, 32), "Fill: ", group)
        Button((x + w - 64 - m, y + 156, 32, 32), partial(fill.changeText, self.parent.selectedTexture), "#", group)
        Button((x + w - 32 - m, y + 156, 32, 32), self.o_textureSelect, "@", group)
        submit = Button((x + m, y + 250, w - 2 * m, 40), overlay.quit, "Create", group)
        overlay.loop()
        if submit():
            if width.intCall() is not None and height.intCall() is not None:
                self.parent.mapgroup = name()
                if fill() == "":
                    self.parent.map = Map([width.intCall(), height.intCall()], self.parent.mapgroup, [32, 32], [50, 50])
                else:
                    self.parent.map = Map([width.intCall(), height.intCall()], self.parent.mapgroup, [32, 32], [50, 50], fill=fill())
                self.parent.tile.rescale()
                self.parent.resetDisplay()
            else:
                Error("Expected integer width/height")

    def o_settings(self):
        group = "Settings"
        w, h, m = 300, 174, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group)
        thumbnailSize = Input((x + m, y + 80, w - 2 * m, 32), "Thumbnail Size: ", group)
        thumbnailSize.changeText(self.parent.thumbnailSize)
        submit = Button((x + m, y + 122, w - 2 * m, 40), overlay.quit, "Save", group)
        overlay.loop()
        if submit() and thumbnailSize.intCall() is not None:
            self.parent.thumbnailSize = thumbnailSize.intCall()
            self.texture.rescaleCustom(thumbnailSize.intCall())

    def o_quit(self):
        group = "Quit"
        w, h, m = 400, 174, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group, exitButton=False)
        Display((x + m, y + 40, w - 2 * m, 32), group, "All unsaved progress will be lost", outline=0)
        Display((x + m, y + 72, w - 2 * m, 32), group, "Are you sure?", outline=0)
        Button((x + m, y + 122, 80, 40), overlay.quit, "No", group)
        yes = Button((x + w - m - 80, y + 122, 80, 40), overlay.quit, "Yes", group)
        overlay.loop()
        if yes(): self.parent.quit()

    def o_textureSelect(self):
        group = "Textures"
        w, h, m = WINDOW[0]-20, WINDOW[1]-100, 10
        x, y = m, WINDOW[1] / 2 - h / 2
        size = self.parent.thumbnailSize
        move = 0
        page = self.parent.latestPage
        overlay = Overlay((x, y, w, h), group)
        search = Input((x + m, y+40, w - 2 * m-80, 32), "Search textures: ", group)
        search.changeText(self.parent.latestSearch)

        thumbnails = Button((x + m + w - 2 * m - 80, y+40, 80, 32),
                            partial(self.o_textureLoad, w, h, m, x, y, size, move, search, group, overlay, page),
                            "Search", group)

        for i in range(36):
            Button((x + m + i*32, y + h - 42, 32, 32),
                   partial(self.o_textureLoad, w, h, m, x, y, size, move, "", group, overlay, i),
                   str(i+1), group)

        thumbnails.returned = self.o_textureLoad(w, h, m, x, y, size, move, search, group, overlay, page)
        overlay.loop()

        if thumbnails() is not None:
            for selected in thumbnails():
                if selected[0]():
                    self.parent.selectedTexture = selected[1]

        self.parent.latestSearch = search()
        self.killall(group)
        self.parent.resetDisplay()

    def o_textureLoad(self, w, h, m, x, y, size, move, search, group, overlay, page):
        self.parent.displayBox.killall(group)
        thumbnails = []
        temp = list(self.texture.data.keys())
        if len(temp) < page+1:
            page = 0
        name = temp[page]

        tw, th, ts = self.texture.data[name]
        my = 0
        for j in range(th):
            for i in range(tw):
                if y + j * size + 40 + 2*size + my > h-3*m:
                    move += tw*size
                    my -= j*size
                thumbnails.append((Display((x + m + size*i + move, y + j * size + 40 + 6*m + my, size, size), group,
                                           image=name+str(i*ts+j), func=overlay.quit), name+str(i*ts+j)))
        self.parent.latestPage = page
        return thumbnails

    def o_loadmap(self):
        group = "Load Map"
        w, h, m = 400, 172, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group)
        Display((x + m, y + 40, w - 2 * m, 32), group, text="Current map will NOT be lost", align="mid", outline=0)
        name = Input((x + m, y + 80, w - 2 * m, 32), "Name: ", group)
        submit = Button((x + m, y + 122, w - 2 * m, 40), overlay.quit, "Load", group)
        overlay.loop()
        if submit():
            if type(name()) is str:
                if name() in Map.manager:
                    self.parent.map.load(name())
                    self.parent.resetDisplay()
                else:
                    Error("{} doesn't exist".format(name()))
            else:
                Error("Expected string")

    def killall(self, group):
        self.parent.button.killall(group)
        self.parent.inputBox.killall(group)
        self.parent.displayBox.killall(group)

    def __group(self):  # Overlays, buttons, and inputboxes expect an unique group string
        self.uniqueGroup += 1
        return str(self.uniqueGroup)
