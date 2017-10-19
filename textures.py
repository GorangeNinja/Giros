import pygame
import os
from settings import *
from maps import *


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

    def __call__(self, filename):
        try:
            return self.scaled[filename]
        except:
            # Name not in dictionary
            return self.scaled["error_alpha.png"]

    def bulk(self):
        # Loads everything in the textures folder
        for filename in os.listdir(self.path):
            self.load(filename)

    def load(self, filename):
        if self.supportedFormats in filename:
            # Sheet format <name_tilesize_sheet.png>
            if "_sheet" in filename:
                if "_alpha" in filename:
                    img = pygame.image.load(self.path + filename).convert_alpha()
                else:
                    img = pygame.image.load(self.path + filename).convert()

                name, sx, sy, useless = filename.split("_")
                sx, sy = int(sx), int(sy)
                w, h = img.get_rect()[2]//sx, img.get_rect()[3]//sy

                i = 0
                for y in range(h):
                    for x in range(w):
                        image = img.subsurface((pygame.Rect(x*sx, y*sy, sx, sy)))
                        self.__add(image, "s-"+name+"-"+str(i))
                        i += 1

                self.data["s-"+name] = [w, h, sx, sy]

            # Transparent image format <name_alpha.png>
            elif "_alpha" in filename:
                img = pygame.image.load(self.path + filename).convert_alpha()
                self.__add(img, filename)

            else:
                img = pygame.image.load(self.path + filename).convert()
                self.__add(img, filename)



    def __add(self, img, filename):
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
