
import random
import utils


class Sensor:
    def __init__(self, world, parentId, sweepTime, detectionRange, entityTypeFilter, pDetect, myForce):
        self.world = world
        self.parentId = parentId
        self.baseSweepTime = sweepTime
        self.detectionRange = detectionRange
        self.entityTypeFilter = entityTypeFilter
        self.pDetect = pDetect
        self.myForce = myForce
        self.elapsedTime = sweepTime  # force a detection on first update

    def update(self, parent, dt):
        searchResults = list()
        self.elapsedTime += dt
        if self.elapsedTime > self.baseSweepTime:
            possibleTargets = self.world.findPlayersInRange(
                parent, self.detectionRange)
            for target in possibleTargets:
                if (target.entityType == self.entityTypeFilter and target.force != self.myForce):
                    diceRoll = random.random()
                    searchResults.append({
                        "targetId": target.playerId,
                        "heading": utils.heading_between_points(parent.x, parent.y, target.x, target.y),
                        "rangeToTarget": utils.distance(parent.x, parent.y, target.x, target.y),
                        "speedOfTarget": target.speed,
                        "diceRoll": diceRoll,
                        "pDetect": self.pDetect,
                        "detected": random.random() < self.pDetect
                    })
            self.elapsedTime = 0.0
        return searchResults
