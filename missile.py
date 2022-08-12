import math
import utils


class Missile:

    imagesByForce = dict()

    def __init__(self, force, shooter, target, speed):
        self.force = force
        self.entityType = "missile"
        self.image = Missile.imagesByForce[force]
        self.playerId = None
        self.x = shooter.x
        self.y = shooter.y
        self.heading = shooter.heading
        self.commandedHeading = None
        self.turnRate = 180.0
        self.speed = speed
        self.target = target
        self.detections = []
        self.ttl = 6  # seconds
        self.runTime = 0.0
        self.state = "ALIVE"

    def setHeading(self, angle):
        self.heading = angle

    def update(self, dt):
        if self.state == "DEAD":
            return

        self.runTime += dt

        if self.runTime > self.ttl:
            self.state = "DEAD"

        # move
        dx = math.cos(math.radians(self.heading))
        dy = math.sin(math.radians(self.heading))
        n = utils.normalize_2d_vector([dx, dy])

        # self.speed *= 0.999

        self.x += n[0] * float(self.speed) * dt
        self.y += n[1] * float(self.speed) * dt

        # should I turn toward my target?
        if self.target.state == "DEAD":
            self.commandedHeading = None
        else:
            self.commandedHeading = utils.heading_between_points(self.x,
                                                         self.y,
                                                         self.target.x,
                                                         self.target.y)

        if self.commandedHeading is not None:
            cmd_hdg = utils.normalize_angle(self.commandedHeading)
            cur_hdg = utils.normalize_angle(self.heading)

            delta_hdg = utils.find_angle_between_headings(cur_hdg,
                                                                  cmd_hdg)

            if delta_hdg > self.turnRate * dt:
                if delta_hdg < 0:
                    self.setHeading(cur_hdg - self.turnRate * dt)
                else:
                    self.setHeading(cur_hdg + self.turnRate * dt)
            else:
                self.commandedHeading = None
