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
    scaled = {}  # Keeps track of all the scaled images, so it only loads them once
    data = {}  # Keeps track of all spritesheets tile width and height and animations fps

    tick = time.time()
    animationSpeed = 10

    def __call__(self, data):
        # data format -> {name, position, resolution, fps}
        #self.fps = int(time.time() * self.animationSpeed - self.tick * self.animationSpeed)
        if str(data["resolution"]) not in self.scaled:
            self.scaled[str(data["resolution"])] = {}

        if data["name"] not in self.scaled[str(data["resolution"])]:
            self.__addScaled(data["name"], data["resolution"], int(data[position))

        return self.scaled[str(resolution)][name][int(position)]

    def bulk(self, folder=""):
        # Loads everything in the textures folder
        for filename in os.listdir(self.path+folder):
            self.load(filename)

    def load(self, filename):
        if self.supportedFormats in filename:
            # Sheet format <name_tilesize_sheet.png>
            if "_sheet" in filename: self.loadSheet("s_", filename)

            # Animation format <name_tilesize_anim.png>
            if "_anim" in filename: self.loadSheet("a_", filename)

            # Transparent image format <name_alpha.png>
            elif "_alpha" in filename:
                img = pygame.image.load(self.path + filename).convert_alpha()
                self.__addNative(img, filename)

            else:
                img = pygame.image.load(self.path + filename).convert()
                self.__addNative(img, filename)

    def loadSheet(self, form, filename):
        img = pygame.image.load(self.path + filename).convert_alpha()

        name, sx, sy, useless = self.__getInfo(filename)
        sx, sy = int(sx), int(sy)
        w, h = img.get_rect()[2] // sx, img.get_rect()[3] // sy

        for y in range(h):
            for x in range(w):
                image = img.subsurface((pygame.Rect(x * sx, y * sy, sx, sy)))
                self.__addNative(image, form + name)

        self.data[form + name] = [w, h, sx, sy]

    def __addNative(self, img, filename):
        try:
            self.native[filename].append(img)

        except KeyError:
            self.native[filename] = [img]

    def __addScaled(self, filename, resolution, position):
        try:
            self.scaled[str(resolution)][filename].append(pygame.transform.scale(self.native[filename][position],
                                                                                 resolution))

        except KeyError:
            self.scaled[str(resolution)][filename] = [pygame.transform.scale(self.native[filename], resolution)]

    def __getInfo(self, filename):
        return filename.split("_")
