# -*- coding: utf-8 -*-
"""
@author: wobblycoder@gmail.com
"""

import pygame

from colors import BLACK


class Artwork:

    def __init__(self, scale=1.0, screenWidth=1920, screenHeight=1080):

        self.assets = dict()
        self.scale = scale
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def loadImage(self, name, path):
        img = pygame.image.load(path).convert()
        self.assets[name] = pygame.transform.scale(img,
                                                   [int(64 * self.scale),
                                                    int(64 * self.scale)])
        self.assets[name].set_colorkey(BLACK)

    def loadBackground(self, name, path):
        img = pygame.image.load(path).convert()
        self.assets[name] = pygame.transform.scale(img,
                                                   [self.screenWidth,
                                                    self.screenHeight])
