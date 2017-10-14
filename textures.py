import pygame
import os
from settings import *
from ui import Error
from maps import *


class Texture:
    window = pygame.display.set_mode((1, 1))

    os.chdir(os.getcwd()+"/textures")
    supportedFormats = ".png"

    path = os.getcwd()
    path += "/"

    native = {}  # Keeps a copy of all the unscaled images
    scaled = {}  # Images scaled to Map.m.tileSize
    custom = {}  # Images scaled to custom size, useful for thumbnails
    data = {}  # Keeps track of spritesheet tile width and height

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
                img = pygame.image.load(self.path + filename).convert_alpha()
                name, size, useless = filename.split("_")
                size = int(size)
                w, h = img.get_rect()[2]//size, img.get_rect()[3]//size

                for x in range(w):
                    for y in range(h):
                        image = img.subsurface((pygame.Rect(x*size, y*size, size, size)))
                        self.__add(image, "s-"+name+str(x*size+y))

                self.data["s-"+name] = [w, h, size]
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

    def addCustom(self, filename, w, h):
        # Rescales an already existing image
        self.custom[filename] = pygame.transform.scale(self.native[filename], (w, h))

    def callCustom(self, filename):
        return self.custom[filename]

    def rescale(self):
        for name in self.native:
            self.scaled[name] = pygame.transform.scale(self.native[name], Map.m.tileSize)

    def rescaleCustom(self, size):
        for name in self.custom:
            self.custom[name] = pygame.transform.scale(self.native[name], (size, size))
