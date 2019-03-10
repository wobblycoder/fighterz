import math
import utils

class Missile:
    def __init__(self, force, shooter, target, speed):
        self.force = force
        self.entityType = "missile"
        self.playerId = None
        self.x = shooter.x
        self.y = shooter.y
        self.heading = shooter.heading
        self.commandedHeading = None
        self.turnRate = 180.0
        self.speed = speed
        self.target = target
        self.detections = []
        self.ttl = 12 # seconds
        self.runTime = 0.0
        self.state = "ALIVE"

    def setHeading(self, angle):
        self.heading = angle

    def update(self, dt):
        #print("missile {1} dt = {0}".format(dt, self))
        if self.state == "DEAD":
            return

        self.runTime += dt

        if self.runTime > self.ttl:
            self.state = "DEAD"

        # move
        dx = math.cos(math.radians(self.heading))
        dy = math.sin(math.radians(self.heading))
        n = utils.normalize2dVector([dx,dy])

        #print("x={0} y={1} speed={2}".format(self.x, self.y, self.speed))
        #print("dx={0} dy={1} n = [{2},{3}]".format(dx, dy, n[0], n[1]))

        self.x += n[0] * float(self.speed) * dt
        self.y += n[1] * float(self.speed) * dt

        #print("new x={0} y={1} speed={2}".format(self.x, self.y, self.speed))

        # should I turn toward my target?
        if self.target.state == "DEAD":
            self.commandedHeading = None
        else:
            self.commandedHeading = utils.computeHeading(self.x, self.y, self.target.x, self.target.y)


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