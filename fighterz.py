#
# fighterz.py
#
# a basic pygame example
#
# wobblycoder@gmail.com
#

from world import World

# from fighter import Fighter
from fighter_v3 import Fighter
import pygame
import demos

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 192, 0)
RED   = (192, 0, 0, 128)
BLUE  = (0, 0, 192, 128)

class FighterzGame:
    def __init__(self, width=1920, height=1080, scale=1.0):
        pygame.init()

        self.screenSize = [width, height]

        self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)

        pygame.display.set_caption('Fighters!')

        # Load and set up graphics.
        self.art = {
            "background": pygame.transform.scale(pygame.image.load("art/desert-background.png").convert(),
                                                 self.screenSize),
            "bluefighter": pygame.transform.scale(pygame.image.load("art/Blue Fighter 64px.png").convert(),
                                                  [int(64 * scale), int(64 * scale)]),
            "redfighter": pygame.transform.scale(pygame.image.load("art/Red Fighter 64px.png").convert(),
                                                 [int(64 * scale), int(64 * scale)]),
            "redmissile": pygame.transform.scale(pygame.image.load("art/Red Missile.png").convert(),
                                                 [int(64 * scale), int(64 * scale)]),
            "bluemissile": pygame.transform.scale(pygame.image.load("art/Blue Missile.png").convert(),
                                                 [int(64 * scale), int(64 * scale)])
        }

        for eNum in range(0,9):
            suffix = "{0:02d}".format(eNum)
            shortname = "explosion" + str(eNum)
            pathname = "art/explosion" + suffix + ".png"
            self.art[shortname] = pygame.transform.scale(pygame.image.load(pathname).convert(),
                                                 [int(64 * scale), int(64 * scale)])

        for image in self.art:
            if image != "background":
                self.art[image].set_colorkey(BLACK)

        self.drawSensorsFlag = False

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


game = FighterzGame(1920, 1080, 0.8)

#demos.OneOnOnePursuit(game.world)
#demos.SpeedTest(game.world)
#demos.HeadingTest(game.world)
demos.ManyVsMany(game.world, 30)


game.mainloop()
