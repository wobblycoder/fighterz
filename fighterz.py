#
# fighterz.py
#
# a basic pygame example
#
# wobblycoder@gmail.com
#

import configparser
import pprint
import pygame
import sys

from artwork import Artwork
from colors import RED, BLUE
from fighter_v3 import Fighter, makeDemoFighter
from missile import Missile
import tests
import utils
from world import World

class FighterzGame:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.done = False
        self.paused = False
        self.drawSensors = False
        self.fullScreen = False
        self.iconScale = 1.0
        self.screen = None
        self.screenSize = [1024, 786]
        self.world = None
        self.selectedPlayer = None

        self.readConfiguration()
        self.initializeGameEngine()
        self.loadGraphics()
        self.createGameWorld()

        if len(sys.argv) > 1:
            self.setupTest()
        else:
            self.setupDemo()


    def mainloop(self):
        ticks = 0
        self.clock = pygame.time.Clock()
        while not self.done:
            self.handleEvents()
            self.drawEverything()
            if not self.paused:
                self.world.update(ticks/1000.0)
                ticks = self.clock.tick(50)
        pygame.quit()

    def drawEverything(self):
        self.drawBackground()
        self.drawFighters()
        self.drawMissiles()
        self.drawExplosions()
        self.drawSelection()
        pygame.display.flip()

    def readConfiguration(self):
        self.config.read("fighterz.cfg")
        self.loadScreenSettings()
        self.loadOptions()
        

    def loadScreenSettings(self):
        if self.config.has_option("Screen", "width"):
            self.screenSize[0] = self.config.getint("Screen", "width")

        if self.config.has_option("Screen", "height"):
            self.screenSize[1] = self.config.getint("Screen", "height")

        if self.config.has_option("Screen", "fullScreen"):
            self.fullScreen = self.config.getboolean("Screen", "fullScreen")
        
        if self.config.has_option("Screen", "iconScale"):
            self.iconScale = self.config.getfloat("Screen", "iconScale")
            print(self.iconScale)
        
    
    def loadOptions(self):
        self.drawSensors = False
        if self.config.has_option("Options", "drawSensors"):
            self.drawSensors = self.config.getboolean("Options", "drawSensors")

        
    def initializeGameEngine(self):
        pygame.init()

        if self.fullScreen:
            self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screenSize)
        
        pygame.display.set_caption('Fighters!')

    
    def loadGraphics(self):
        self.art = Artwork(scale=self.iconScale,
                           screenWidth=self.screenSize[0],
                           screenHeight=self.screenSize[1])

        icons = self.config.items("Icons")

        for icon in icons:
            self.art.loadImage(icon[0], icon[1])

        backgrounds = self.config.items("Backgrounds")
        chosen_background = self.config.get("Backgrounds", "choice")
        self.art.loadBackground("background", self.config.get("Backgrounds", chosen_background))

        Fighter.imagesByForce = {
            BLUE : self.art.assets["bluefighter"],
            RED : self.art.assets["redfighter"]
        }
            
        Missile.imagesByForce = {
            BLUE : self.art.assets["bluemissile"],
            RED : self.art.assets["redmissile"]
        }
            
    
    def createGameWorld(self):
        maxWorldX = 1000.0
        maxWorldY = maxWorldX * self.screenSize[1] / self.screenSize[0]
        self.world = World([maxWorldX, maxWorldY])

    def setupDemo(self):

        if (self.config.has_option("Demo", "enabled") and
            self.config.getboolean("Demo", "enabled")):

            redQty = self.config.getint("Demo", "red.qty")
            blueQty = self.config.getint("Demo", "blue.qty")

            for i in range(redQty):
                rf = makeDemoFighter(RED, self.config, self.world)
                self.world.addPlayer(rf)

            for j in range(blueQty):
                bf = makeDemoFighter(BLUE, self.config, self.world)
                self.world.addPlayer(bf)

    def setupTest(self):
        try:
            testFunction = getattr(tests, sys.argv[-1])
            self.world.addPlayers(testFunction())
        except:
            pass

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.selectedPlayer = self.findNearestPlayer(event.pos)
            elif event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_s:
                    self.drawSensors = not self.drawSensors
                if event.key in [pygame.K_p, pygame.K_SPACE]:
                    self.paused = not self.paused
                    if not self.paused:
                        self.clock = pygame.time.Clock()


    def findNearestPlayer(self, eventPos):

        ids = list(self.world.players.keys())
        p1 = self.world.players[ids[0]]
        sx, sy = self.translateWorldToScreenCoordinates(p1.x, p1.y)
        nearestDistance = utils.computeDistance(eventPos[0], eventPos[1], sx, sy)
        closest = p1

        for playerId in ids[1:]:
            p = self.world.players[playerId]
            sx, sy = self.translateWorldToScreenCoordinates(p.x, p.y)
            d = utils.computeDistance(eventPos[0], eventPos[1], sx, sy)
            if d < nearestDistance:
                closest = p
                nearestDistance = d

        if nearestDistance < 64 and closest.state != "DEAD":
            return closest

        return None


    def drawBackground(self):
        self.screen.blit(self.art.assets["background"], [0, 0])


    def drawFighters(self):
        for playerId in self.world.players:
            player = self.world.players[playerId]
            if player.state != "DEAD":
                self.drawPlayer(player)


    def drawMissiles(self):
        for missileId in self.world.weapons:
            missile = self.world.weapons[missileId]
            if missile.state != "DEAD":
                self.drawPlayer(missile)


    def drawExplosions(self):
        for explosionNumber in self.world.explosions:
            explosion = self.world.explosions[explosionNumber]
            self.drawExplosion(explosion)

        
    def drawExplosion(self, explosion):
        imageName = "explosion" + str(explosion["phase"] % 9)
        image = self.art.assets[imageName]
        px, py = self.translateWorldToScreenCoordinates(explosion["x"], explosion["y"])
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2
        self.screen.blit(image, [blitx, blity])


    def drawPlayer(self, player):
        image = player.image
        px, py = self.translateWorldToScreenCoordinates(player.x, player.y)
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2

        if self.drawSensors:
            if hasattr(player, "searchResults"):
                for detection in player.searchResults:
                    if detection["detected"] and detection["targetId"] in self.world.players:

                        dx, dy = self.translateWorldToScreenCoordinates(self.world.players[detection["targetId"]].x,
                                                                        self.world.players[detection["targetId"]].y)

                        pygame.draw.line(self.screen, player.force, [px, py+1], [dx, dy+1], 5)


        rotatedImage = self.rotateImage(image, player.heading)
        self.screen.blit(rotatedImage, [blitx, blity])


    def drawSelection(self):
        if self.selectedPlayer is not None and self.selectedPlayer.state != "ALIVE":
            self.selectedPlayer = None
            return

        if self.selectedPlayer is not None:
            px, py = self.translateWorldToScreenCoordinates(self.selectedPlayer.x, self.selectedPlayer.y)
            pygame.draw.circle(self.screen,
                               (0,255,0,128),
                               (int(px), int(py)),
                               int(self.selectedPlayer.image.get_width()/2),
                               2)


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


game = FighterzGame()
game.mainloop()
