#
# fighterz.py
#
# a basic pygame example
#
# wobblycoder@gmail.com
#

import configparser
import glob
import os

from world import World

# from fighter import Fighter
from fighter_v3 import Fighter
from artwork import Artwork
import pygame
import demos

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 192, 0)
RED   = (192, 0, 0, 128)
BLUE  = (0, 0, 192, 128)

class FighterzGame:

    def __init__(self):
        self.readConfiguration()
        self.initializeGameEngine()
        self.loadGraphics()
        self.createGameWorld()
        
        
    def readConfiguration(self):
        # set defaults
        self.drawSensorsFlag = False
        self.screenSize = [1024, 768]

        # TODO : read the config file
        

    
    def initializeGameEngine(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        pygame.display.set_caption('Fighters!')

    
    def loadGraphics(self):
        pass
        # TODO: load and scale the images in the config file
    

    
    def createGameWorld(self):
        maxWorldX = 1000.0
        maxWorldY = maxWorldX * self.screenSize[1] / self.screenSize[0]
        self.world = World([maxWorldX, maxWorldY])
        
        
    
        

    def drawExplosion(self, explosion):
        imageName = "explosion" + str(explosion["phase"] % 9)
        image = self.art[imageName]
        px, py = self.translateWorldToScreenCoordinates(explosion["x"], explosion["y"])
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2
        self.screen.blit(image, [blitx, blity])

    def drawPlayer(self, player):
        imageName = player.force + player.entityType
        image = self.art[imageName]
        px, py = self.translateWorldToScreenCoordinates(player.x, player.y)
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2

        if self.drawSensorsFlag:
            if hasattr(player, "searchResults"):
                for detection in player.searchResults:
                    if detection["detected"] and detection["targetId"] in self.world.players:

                        dx, dy = self.translateWorldToScreenCoordinates(self.world.players[detection["targetId"]].x,
                                                                        self.world.players[detection["targetId"]].y)

                        if player.force == "blue":
                            pygame.draw.line(self.screen, BLUE, [px, py+1], [dx, dy+1], 5)
                        if player.force == "red":
                            pygame.draw.line(self.screen, RED, [px, py-1], [dx, dy-1], 5)

        rotatedImage = self.rotateImage(image, player.heading)
        self.screen.blit(rotatedImage, [blitx, blity])

    def rotateImage(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def translateWorldToScreenCoordinates(self, x, y):
        newX = ((x - self.world.minX) / (self.world.maxX - self.world.minX)) * self.screenSize[0]
        newY = self.screenSize[1] - ((y - self.world.minY) / (self.world.maxY - self.world.minY)) * self.screenSize[1]
        return newX, newY

    def mainloop(self):

        ticks = 0

        clock = pygame.time.Clock()

        done = False

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_s:
                        self.drawSensorsFlag = not self.drawSensorsFlag
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                        #   click_sound.play()

            # draw our background
            self.screen.blit(self.art["background"], [0, 0])

            self.world.update(ticks/1000.0)

            # draw our moving objects
            for playerId in self.world.players:
                player = self.world.players[playerId]
                if player.state != "DEAD":
                    self.drawPlayer(player)

            for missileId in self.world.weapons:
                missile = self.world.weapons[missileId]
                if missile.state != "DEAD":
                    self.drawPlayer(missile)

            for explosionNumber in self.world.explosions:
                explosion = self.world.explosions[explosionNumber]
                self.drawExplosion(explosion)

            pygame.display.flip()
            # self.world.sendThoughtBubble("dt = " + str(ticks))
            ticks = clock.tick(50)

        pygame.quit()
        
    def setupGraphics(self):

        icons = {
            "bluefighter" : "art/Blue Fighter 64px.png"
            "redfighter" : "art/Red Fighter 64px.png"
            "redmissile" : "art/Red Missile.png"
            "bluemissile" : "art/Blue Missile.png"
        }
        
        for eNum in range(0,9):
            suffix = "{0:02d}".format(eNum)
            shortname = "explosion" + str(eNum)
            pathname = "art/explosion" + suffix + ".png"
            icons[shortname] = pathname
        

        self.art = Artwork()
        self.art.addImagery(
            assets = icons,
            background = "art/desert-background.png",
        )

        pass


game = FighterzGame(1920, 1080, 0.8)

#demos.OneOnOnePursuit(game.world)
#demos.SpeedTest(game.world)
#demos.HeadingTest(game.world)
demos.ManyVsMany(game.world, 30)


game.mainloop()
