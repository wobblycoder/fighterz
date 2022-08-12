import math
import utils


class World:
    def __init__(self, mySize):
        self.players = dict()
        self.playerId = 0
        self.minX = -mySize[0]
        self.maxX = mySize[0]
        self.minY = -mySize[1]
        self.maxY = mySize[1]
        self.runTime = 0.0
        self.weapons = dict()
        self.weaponId = 0
        self.explosions = dict()
        self.explosionId = 0

        self.logfile = open("thoughts.log", "w")

    def __del__(self):
        self.logfile.close()

    def addExplosion(self, x, y):
        self.explosions[self.explosionId] = {"x": x, "y": y, "phase": 0}
        self.explosionId += 1

    def addPlayer(self, p):
        self.players[self.playerId] = p
        p.playerId = self.playerId
        self.playerId += 1
        p.setWorld(self)

    def addPlayers(self, players):
        for player in players:
            self.players[self.playerId] = player
            player.playerId = self.playerId
            self.playerId += 1
            player.setWorld(self)

    def addWeapon(self, missile):
        self.weapons[self.weaponId] = missile
        missile.playerId = self.weaponId
        self.weaponId += 1

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def heading(self, p1, p2):
        return utils.heading_between_points(p1.x, p1.y, p2.x, p2.y)

    def findPlayersInRange(self, seeker, detectionRange):
        foundPlayers = list()
        for tgtId in self.players:
            tgt = self.players[tgtId]
            if tgtId != seeker.playerId and tgt.state != "DEAD":
                rangeToTarget = self.distance(seeker, tgt)
                if rangeToTarget <= detectionRange:
                    foundPlayers.append(tgt)
        return foundPlayers

    def sendThoughtBubble(self, thought):
        self.logfile.write("{0:.3f} : {1}\n".format(self.runTime, thought))

    def update(self, dt):

        # remove anyone killed in the last update
        deadPlayers = []
        for playerId in self.players:
            player = self.players[playerId]
            if player.state == "DEAD":
                deadPlayers.append(playerId)

        deadWeapons = []
        for missileId in self.weapons:
            missile = self.weapons[missileId]
            if missile.state == "DEAD":
                deadWeapons.append(missile.playerId)

        for deadPlayer in deadPlayers:
            del self.players[deadPlayer]

        for deadWeapon in deadWeapons:
            del self.weapons[deadWeapon]

        for playerId in self.players:
            player = self.players[playerId]
            player.update(dt)

        for missileId in self.weapons:
            missile = self.weapons[missileId]
            missile.update(dt)
            for otherId in self.players:
                other = self.players[otherId]
                if other.force != missile.force:
                    if self.distance(missile, other) < 25:
                        missile.state = "DEAD"
                        other.setSpeed(0)
                        other.state = "DEAD"
                        self.addExplosion(other.x, other.y)

        # update the explosions
        oldExplosions = list()
        for expNum in self.explosions:
            explosion = self.explosions[expNum]
            if explosion["phase"] == 9:
                oldExplosions.append(expNum)
            explosion["phase"] += 1
        for n in oldExplosions:
            del self.explosions[n]
