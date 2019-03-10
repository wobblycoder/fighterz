import math
import utils
import random

from missile import Missile
from sensor import Sensor

class Fighter:

    def __init__(self, force):

        self.entityType = "fighter"
        self.force = force
        self.playerId = None

        self.world = None

        self.state = "ALIVE"
        self.mode = "SEARCH"  # or PURSUIT, or FIRE

        self.x = 0
        self.y = 0
        self.speed = 0
        self.heading = 0
        self.commandedHeading = None

        self.turnRate = 90.0

        self.sensors = list()

        self.weapons = list()
        self.shotsAvailable = 0
        self.shotRange = 0
        self.shotDelay = 3.0
        self.shotSpeed = 0
        self.currentShotDelay = 0.0

        # search parameters
        self.searchResults = []

        # pursuit parameters
        self.elapsedPursuitTime = 0.0
        self.pursuitTime = 5.0
        self.pursuitRange = 2000.0

    def doSearch(self, dt):

        if len(self.searchResults) != 0:
            # sort targets by range to target

            foundPDT = False
            self.searchResults.sort(key=lambda x: x["rangeToTarget"], reverse=False)

            seenTargets = list()
            for t in self.searchResults:
                if t["detected"]:
                    seenTargets.append(t)

            if len(seenTargets) > 0:
                if not foundPDT:
                    self.primaryTarget = seenTargets[0]
                    foundPDT = True

                if foundPDT:
                    # if my best target is within pursuit range, transition to pursuit
                    #print("Target at heading {0}".format(self.primaryTarget["heading"]))

                    if self.primaryTarget["rangeToTarget"] < self.pursuitRange:
                        self.mode = "PURSUIT"
                        #print("Transitioning to PURSUIT")

                # for res in self.searchResults: print(res)

        # should I turn back toward the engagement zone?
        if utils.computeDistance(self.x, self.y, 0, 0) > math.hypot(self.world.maxX, self.world.maxY) * 0.9:
            newheading = utils.computeHeading(self.x, self.y, 0, 0)
            newheading += random.randint(-20, 20)
            self.setHeading(newheading)

    def doPursuit(self, dt):

        self.elapsedPursuitTime += dt

        if self.elapsedPursuitTime > self.pursuitTime:
            self.mode = "SEARCH"
            self.elapsedPursuitTime = 0.0
            return

        self.commandedHeading = self.primaryTarget["heading"]

        cmdHdgNormalized = utils.normalizeAngle(self.commandedHeading)
        curHdgNormalized = utils.normalizeAngle(self.heading)

        deltaHeading = utils.computeSmallestAngleBetweenHeadings(curHdgNormalized, cmdHdgNormalized)

        # print("commanded: {0} current: {1} delta: {2}".format(cmdHdgNormalized, curHdgNormalized, deltaHeading))

        if abs(deltaHeading) > self.turnRate * dt:
            if deltaHeading < 0:
                self.setHeading(curHdgNormalized - self.turnRate * dt)
            else:
                self.setHeading(curHdgNormalized + self.turnRate * dt)
        else:
            self.setHeading(cmdHdgNormalized)
            self.setSpeed(self.primaryTarget["speedOfTarget"])

        if self.primaryTarget["rangeToTarget"] < self.shotRange and abs(self.primaryTarget["heading"]) < 20:
            self.mode = "FIRE"

    def doFire(self, dt):
        if self.shotsAvailable > 0 and self.currentShotDelay == 0 and self.primaryTarget is not None:
            if self.primaryTarget["targetId"] in self.world.players:
                tgt = self.world.players[self.primaryTarget["targetId"]]
                hdgToTarget = utils.computeHeading(self.x, self.y, tgt.x, tgt.y)

                # hdgDiff = utils.normalizeAngle(abs(self.heading - hdgToTarget))

                hdgDiff = utils.computeSmallestAngleBetweenHeadings(self.heading, hdgToTarget)

                print("me {0}   tgt {1}   hdg {2}   hdgToTgt {3}   diff {4}".format(self.playerId,
                                                                                    tgt.playerId,
                                                                                    self.heading,
                                                                                    hdgToTarget,
                                                                                    hdgDiff))

                if self.primaryTarget["rangeToTarget"] < self.shotRange and hdgDiff < 30: # or hdgDiff > 345):
                    if self.primaryTarget["targetId"] in self.world.players:
                        self.world.sendThoughtBubble("Firing missile from position {0},{1}".format(self.x, self.y))
                        missile = Missile(self.force, self, self.world.players[self.primaryTarget["targetId"]], self.shotSpeed)
                        self.world.addWeapon(missile)
                        self.currentShotDelay = self.shotDelay
                        self.shotsAvailable -= 1

    def setHeading(self, hdg):
        self.heading = hdg

    def setPosition(self,x,y):
        self.x = x
        self.y = y

    def setWorld(self, world):
        self.world = world
        for sensor in self.sensors:
            sensor.world = world

    def addSensor(self, sweepTime, detectionRange, entityTypeFilter, pDetect):
        self.sensors.append(Sensor(self.world, self.playerId, sweepTime, detectionRange, entityTypeFilter, pDetect, self.force))

    def addWeaponLoadout(self, qty, rng, spd=100):
        self.shotsAvailable = qty
        self.shotRange = rng
        self.shotSpeed = spd
        #for i in range(qty):
        #    self.weapons.append(Missile(rng))

    def setSpeed(self, speed):
        self.speed = speed

    def updatePosition(self, dt):
        dx = math.cos(math.radians(self.heading))
        dy = math.sin(math.radians(self.heading))
        n = utils.normalize2dVector([dx,dy])

        #print("fighter\n\tx={0} y={1} speed={2}".format(self.x, self.y, self.speed))
        #print("\tdx={0} dy={1} n = [{2},{3}]".format(dx, dy, n[0], n[1]))

        self.x += n[0] * self.speed * dt
        self.y += n[1] * self.speed * dt

        #print("\tnew x={0} y={1} speed={2}".format(self.x, self.y, self.speed))

        if self.commandedHeading is not None:
            cmdHdgNormalized = utils.normalizeAngle(self.commandedHeading)
            curHdgNormalized = utils.normalizeAngle(self.heading)

            deltaHeading = utils.computeSmallestAngleBetweenHeadings(curHdgNormalized, cmdHdgNormalized)

            if deltaHeading > self.turnRate * dt:
                if deltaHeading < 0:
                    self.setHeading(curHdgNormalized - self.turnRate * dt)
                else:
                    self.setHeading(curHdgNormalized + self.turnRate * dt)
            else:
                self.commandedHeading = None

    def updateSensors(self, dt):
        self.searchResults = []
        for sensor in self.sensors:
            self.searchResults.extend(sensor.update(parent=self, dt=dt))

    def updateTimers(self, dt):
        if self.currentShotDelay < dt:
            self.currentShotDelay = 0
        else:
            self.currentShotDelay -= dt

    def update(self, dt):
        self.updatePosition(dt)
        self.updateSensors(dt)
        self.updateTimers(dt)
        self.doSearch(dt)

        if self.mode == "PURSUIT":
            self.doPursuit(dt)

        if self.mode == "FIRE":
            self.doFire(dt)


