import pygame
import os
from settings import *
from maps import *
import time


class Texture:
    window = pygame.display.set_mode((1, 1))

    os.chdir(os.getcwd()+"/images")
    supportedFormats = ".png"

    path = os.getcwd()
    path += "/"

    native = {}  # Keeps a copy of all the unscaled images
    scaled = {}  # Images scaled to Map.m.tileSize
    custom = {}  # Images scaled to custom size, useful for thumbnails
    data = {}  # Keeps track of all spritesheets tile width and height

    tick = time.time()
    animationSpeed = 10

    def __call__(self, filename):
        self.fps = int(time.time() * self.animationSpeed - self.tick * self.animationSpeed)

        temp = filename.split("-")
        if temp[0] == "a":
            return self.scaled[temp[0]+"-"+temp[1]+"-"+str(self.fps%(self.data[temp[0]+"-"+temp[1]][0]))]
        return self.scaled[filename]

    def bulk(self):
        # Loads everything in the textures folder
        for filename in os.listdir(self.path):
            self.load(filename)

    def load(self, filename):
        if self.supportedFormats in filename:
            # Sheet format <name_tilesize_sheet.png>
            if "_sheet" in filename: self.loadSheet("s-", filename)

            # Animation format <name_tilesize_anim.png>
            if "_anim" in filename: self.loadSheet("a-", filename)

            # Transparent image format <name_alpha.png>
            elif "_alpha" in filename:
                img = pygame.image.load(self.path + filename).convert_alpha()
                self.__add(img, filename)

            else:
                img = pygame.image.load(self.path + filename).convert()
                self.__add(img, filename)

    def loadSheet(self, form, filename):
        img = pygame.image.load(self.path + filename).convert_alpha()

        name, sx, sy, useless = filename.split("_")
        sx, sy = int(sx), int(sy)
        w, h = img.get_rect()[2] // sx, img.get_rect()[3] // sy

        i = 0
        for y in range(h):
            for x in range(w):
                image = img.subsurface((pygame.Rect(x * sx, y * sy, sx, sy)))
                self.__add(image, form + name + "-" + str(i))
                i += 1

        self.data[form + name] = [w, h, sx, sy]

    def __add(self, img, filename):
        try:
            self.native[filename].append(img)
            self.scaled[filename].append(pygame.transform.scale(img, Map.m.tileSize))
        except KeyError:
            self.native[filename] = img
            self.scaled[filename] = pygame.transform.scale(img, Map.m.tileSize)

    def addCustom(self, group, filename, w, h):
        # Rescales an already existing image
        self.custom[group][filename] = pygame.transform.scale(self.native[filename], (w, h))

    def callCustom(self, group, filename):
        return self.custom[group][filename]

    def rescale(self):
        for name in self.native:
            self.scaled[name] = pygame.transform.scale(self.native[name], Map.m.tileSize)

    def rescaleCustom(self, group, size):
        for name in self.custom[group]:
            self.custom[group][name] = pygame.transform.scale(self.native[name], (size, size))
