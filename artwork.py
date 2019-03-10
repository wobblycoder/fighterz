# -*- coding: utf-8 -*-
"""
@author: wobblycoder@gmail.com
"""

class Artwork:
    
    def __init__(self, scale=1.0, screenWidth=1920, screenHeight=1080):
        
        self.assets = dict()
        
        self.colors = {
            "WHITE" : (255, 255, 255),
            "BLACK" : (0, 0, 0),
            "GREEN" : (0, 192, 0),
            "RED "  : (192, 0, 0, 128),
            "BLUE"  : (0, 0, 192, 128),
        }
        
        self.scale = scale
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        
        
        
    def loadSprite(self, name, path):

        self.assets[name] = pygame.transform.scale(pygame.image.load(path).convert(),
                                                   [int(64 * self.scale), 
                                                    int(64 * self.scale)])
        self.assets[name].set_colorkey(BLACK)

        for eNum in range(0,9):
            shortname = "explosion" + str(eNum)
            pathname = "art/explosion{0:02d}.png".format(eNum)
            self.assets[shortname] = pygame.transform.scale(pygame.image.load(pathname).convert(),
                                                 [int(64 * scale), int(64 * scale)])

    def loadBackground(name, path)    
        self.assets[name] = pygame.transform.scale(pygame.image.load(path).convert(),
                                                 [self.screenWidth, screenHeight])


        
