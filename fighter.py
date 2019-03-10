import math
import random

from operator import itemgetter


class Fighter:
    def __init__(self):
        self.playerId = None
        self.force = "blue"
        self.entityType = "fighter"
        self.playerId = None
        self.x = 0
        self.y = 0
        self.heading = 0
        self.commandedHeading = None
        self.turnRate = 60.0
        self.speed = 0
        self.detectionRange = 300  # see everything with math.hypot(screen width, screen height)
        self.pDetect = 0.5
        self.world = None
        self.targets = dict()
        self.detections = dict()
        self.bestTarget = None
        self.currentTarget = None

    def chooseBestTarget(self):
        tgtList = list(self.targets.values())
        if len(tgtList) > 0:
            sorted(tgtList, key=itemgetter("range"))
            self.bestTarget = (tgtList[0]["id"], tgtList[0]["heading"])

    def search(self, runTime):
        if self.world is not None:
            self.detections = dict()
            # who can I detect right now
            detectedTargets, missedTargets = self.world.findTargetsInRange(self.playerId, self.detectionRange,
                                                                           self.pDetect)
            for newTarget in detectedTargets:
                rngToTgt = newTarget[0]
                idOfTgt = newTarget[1]
                hdgToTgt = newTarget[2]
                if idOfTgt not in self.targets:
                    self.targets[idOfTgt] = dict()
                    self.world.sendThoughtBubble(
                        "Platform {0} new target!  Range: {1}  Heading {2}".format(self.playerId, rngToTgt, hdgToTgt))
                self.targets[idOfTgt] = {"id": idOfTgt, "time": runTime, "range": rngToTgt, "heading": hdgToTgt}
                self.detections[idOfTgt] = {"id": idOfTgt, "time": runTime, "range": rngToTgt, "heading": hdgToTgt}

            # remove targets I have not seen in a while
            staleTargets = list()
            for oldTarget in self.targets:
                if abs(self.targets[oldTarget]["time"] - runTime) > 30.0:
                    staleTargets.append(oldTarget)

            for staleTarget in staleTargets:
                del self.targets[staleTarget]

    def update(self, runTime):
        # wrap around the edges of the screen
        if self.y < self.world.minY:
            self.y = self.world.maxY
        elif self.y > self.world.maxY:
            self.y = self.world.minY

        if self.x < self.world.minX:
            self.x = self.world.maxX
        elif self.x > self.world.maxX:
            self.x = self.world.minX

        # look for targets and calculate a new heading toward the nearest
        if self.world is not None:
            self.search(runTime)
            self.chooseBestTarget()
            if self.bestTarget is not None:
                self.commandedHeading = self.bestTarget[1]
                if abs(self.commandedHeading - self.heading) < 0.1:
                    self.heading = self.commandedHeading
                    self.commandedHeading = None

                #else:
                #    self.world.sendThoughtBubble(
                #        "Platform {0} changing heading.  Was {1:.2f} Now {2:.2f}".format(self.playerId, self.heading,
                #                                                                         self.commandedHeading))

        if self.commandedHeading is not None:
            deltaHeading = abs(self.commandedHeading - self.heading)
            if deltaHeading > self.turnRate / 60.0:
                if self.commandedHeading < self.heading:
                    self.heading -= self.turnRate / 60.0
                elif self.commandedHeading > self.heading:
                    self.heading += self.turnRate / 60.0
            else:
                self.heading = self.commandedHeading
                self.commandedHeading = None

        # move
        self.x += math.sin(math.radians(self.heading)) * self.speed / 60.0
        self.y += -math.cos(math.radians(self.heading)) * self.speed / 60.0

