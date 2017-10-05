import pygame
import os
from settings import *
from errors import *
from maps import *


class Texture:
    window = pygame.display.set_mode((1, 1))

    os.chdir(os.getcwd()+"/textures")
    supportedFormats = ".png"

    path = os.getcwd()
    path += "/"

    native = {}
    scaled = {}
    custom = {}

    def __call__(self, filename):
        try:
            return self.scaled[filename]
        except:
            # Name not in dictionary
            return self.scaled["error_alpha.png"]

    def bulk(self):
        for filename in os.listdir(self.path):
            self.load(filename)

    def load(self, filename):
        if self.supportedFormats in filename:
            if "alpha" in filename:
                img = pygame.image.load(self.path + filename).convert_alpha()
            else:
                img = pygame.image.load(self.path + filename).convert()

            self.native[filename] = img
            self.scaled[filename] = pygame.transform.scale(img, Map.m.tileSize)

    def loadCustom(self, filename, w, h):
        self.custom[filename] = pygame.transform.scale(self.native[filename], (w, h))

    def callCustom(self, filename):
        try:
            return self.custom[filename]
        except:
            # Name not in dictionary
            return self.scaled["error_alpha.png"]

    def rescale(self):
        for name in self.native:
            self.scaled[name] = pygame.transform.scale(self.native[name], Map.m.tileSize)
