import pygame
from tiles import *
import matrix
from settings import *
from maps import *
from functools import partial
from textures import Texture
from ui import *
import copy


# This is where dreams come to die
class Prefab:
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
        Button((x + w - 64 - m, y + 156, 32, 32),
               partial(fill.changeText, self.parent.sList[self.parent.sCurrent]), "#", group)
        Button((x + w - 32 - m, y + 156, 32, 32), self.o_textureSelect, "@", group)
        submit = Button((x + m, y + 250, w - 2 * m, 40), overlay.quit, "Create", group)
        overlay.loop()
        if submit():
            if width.intCall() is not None and height.intCall() is not None:
                self.parent.mapgroup = name()
                if fill() == "":
                    self.parent.map = Map([width.intCall(), height.intCall()], self.parent.mapgroup)
                else:
                    self.parent.map = Map([width.intCall(), height.intCall()], self.parent.mapgroup, fill=fill())
                self.parent.tile.rescale()
                self.parent.resetDisplay()
            else:
                Message("Expected integer width/height")

    def o_settings(self):
        group = "Settings"
        w, h, m = 600, 400, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group)
        mapName = Input((x + m, y + 40, w-2*m, 32), "Map Name: ", group)
        mapName.changeText(Map.m.name)
        thumbnailSize = Input((x + m, y + 80, w-2*m, 32), "Thumbnail Size: ", group)
        thumbnailSize.changeText(self.parent.thumbnailSize)
        submit = Button((x + m, y + h - 40 - m, w - 2 * m, 40), overlay.quit, "Save", group)

        uilist = []
        for i in range(12):
            uilist.append([Input((0, 0, w - 4 * m, 32), "Test{}".format(i), group)])
        Scroll((x + m, y + h//2 - m, w - 2 * m, 150), uilist, group)
        overlay.loop()
        if submit():
            if thumbnailSize.intCall() is not None:
                self.parent.thumbnailSize = thumbnailSize.intCall()
            if mapName() is not "":
                oldName = Map.m.name
                Map.m.name = mapName()
                Map.manager[mapName()] = Map.manager.pop(oldName)
                self.parent.resetDisplay()

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
        group = "Thumbnails"
        w, h, m = WINDOW[0]-20, WINDOW[1]-100, 10
        x, y = m, WINDOW[1] / 2 - h / 2
        size = self.parent.thumbnailSize
        overlay = Overlay((x, y, w, h), group)
        bList = []

        for i in range(len(Texture.data)):
            bList.append(Button((x + m + i*32, y + h - 42, 32, 32),
                   partial(self.o_textureLoad, w, h, m, x, y, size, group, overlay, i),
                   str(i+1), group))

        bList[self.parent.page].run()
        overlay.loop()

        if bList[self.parent.page]() is not None:
            for line in bList[self.parent.page]():
                for img in line:
                    if img():
                        self.parent.sList[self.parent.sCurrent] = img.image

        self.parent.resetDisplay()

    def o_textureLoad(self, w, h, m, x, y, size, group, overlay, page):
        self.parent.displayBox.killall(group)
        line = []
        column = []
        temp = list(self.texture.data.keys())
        if len(temp) < page+1:
            page = 0
        name = temp[page]

        tw, th, tsx, tsy = self.texture.data[name]
        p = 0
        for j in range(th):
            for i in range(tw):
                line.append(Display((i*size, 0, size, size), group,
                                    image=name+"-"+str(p), func=overlay.quit))
                p += 1
            column.append(line)
            line = []
        self.parent.page = page
        Scroll((x + m, y + 40, w - 2 * m, h-100), column, group, movespeed=size)
        return column

    def o_loadmap(self):
        group = "Load Map"
        w, h, m = 400, 500, 10
        x, y = WINDOW[0] / 2 - w / 2, WINDOW[1] / 2 - h / 2
        overlay = Overlay((x, y, w, h), group)
        Display((x + m, y + 40, w - 2 * m, 32), group, text="Current map will NOT be lost", align="m", outline=0)
        uilist = []
        for i, level in enumerate(Map.manager):
            uilist.append([Display((0, 0, w - 2 * m - 52, 32), group, level),
                           Button((w - 2 * m - 52, 0, 32, 32), overlay.quit, "#", group)])

        Scroll((x + m, y + 80, w - 2 * m, 406), uilist, group)
        overlay.loop()
        for element in uilist:
            if element[1]():
                self.parent.map.load(element[0].text)
                self.parent.resetDisplay()
