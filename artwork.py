# -*- coding: utf-8 -*-
"""
@author: wobblycoder@gmail.com
"""

import pygame

from colors import *

class Artwork:
    
    def __init__(self, scale=1.0, screenWidth=1920, screenHeight=1080):
        
        self.assets = dict()
        self.scale = scale
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        
    def loadImage(self, name, path):

        self.assets[name] = pygame.transform.scale(pygame.image.load(path).convert(),
                                                   [int(64 * self.scale), 
                                                    int(64 * self.scale)])
        self.assets[name].set_colorkey(BLACK)

    def loadBackground(self, name, path):
        self.assets[name] = pygame.transform.scale(pygame.image.load(path).convert(),
                                                 [self.screenWidth, self.screenHeight])


        
