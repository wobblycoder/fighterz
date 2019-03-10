from fighter_v3 import Fighter
import random

def makeFighter(world, force):
    p = Fighter(force)
    y = random.randint(int(0.8 * world.minY), int(0.8 * world.maxY))
    p.setSpeed(100)

    if force == "blue":
        x = random.randint(world.minX + 64, world.minX * 0.8)
        hdg = random.randint(-15, 15)
        p.turnRate = 120.0
        p.addSensor(sweepTime=0.25,
                    detectionRange=750.0,
                    entityTypeFilter="fighter",
                    pDetect=0.75)

        p.addWeaponLoadout(qty=12, rng=350, spd=250)

    else:
        x = random.randint(world.maxX * 0.8, world.maxX - 64)
        hdg = random.randint(180 - 15, 180 + 15)
        p.turnRate = 60.0
        p.addSensor(0.25, 750.0, "fighter", 0.75)
        p.addWeaponLoadout(6,250,250)

    p.setPosition(x, y)
    p.setHeading(hdg)

    return p

def ManyVsMany(world, perSide=20):

    for redCount in range(perSide):
        world.addPlayer(makeFighter(world, "red"))

    for blueCount in range(perSide):
        world.addPlayer(makeFighter(world, "blue"))

def HeadingTest(world):
    x = -900
    for h in range(0,360,15):
        p = Fighter("blue")
        p.setPosition(x=x, y=0)
        p.setSpeed(200)
        p.setHeading(h)
        p.detectRange = 250
        p.pDetect = 0.5
        x += 64
        world.addPlayer(p)

def OneOnOnePursuit(world):
    p = Fighter("blue")
    p.setPosition(-900.0, 0)
    p.setSpeed(100)
    p.setHeading(0)
    p.addSensor(1.0, 600.0, "fighter", 1.0)
    # p.addWeaponLoadout(1, 500, 120)

    q = Fighter("red")
    q.setPosition(900,0)
    q.setHeading(180)
    q.setSpeed(100)
    q.addSensor(1.5, 400.0, "fighter", 0.75)

    world.addPlayer(p)
    world.addPlayer(q)

def SpeedTest(world):

    for y in range(0,700):
        p = Fighter("blue")
        p.setPosition(-1000.0, y)
        p.setSpeed(y)
        p.setHeading(0)

        q = Fighter("blue")
        q.setPosition(-1000.0, -y)
        q.setSpeed(y)
        q.setHeading(0)

        world.addPlayer(p)
        world.addPlayer(q)

