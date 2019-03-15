from fighter_v3 import Fighter
from colors import *

import random

def HeadingTest(world):
    x = -900
    for h in range(0,360,15):
        p = Fighter(BLUE)
        p.setPosition(x=x, y=0)
        p.setSpeed(200)
        p.setHeading(h)
        p.detectRange = 250
        p.pDetect = 0.5
        x += 64
        world.addPlayer(p)

def OneOnOnePursuit(world):
    p = Fighter(BLUE)
    p.setPosition(-900.0, 0)
    p.setSpeed(100)
    p.setHeading(0)
    p.addSensor(1.0, 600.0, "fighter", 1.0)
    # p.addWeaponLoadout(1, 500, 120)

    q = Fighter(RED)
    q.setPosition(900,0)
    q.setHeading(180)
    q.setSpeed(100)
    q.addSensor(1.5, 400.0, "fighter", 0.75)

    world.addPlayer(p)
    world.addPlayer(q)

def SpeedTest(world):

    for y in range(0,700):
        p = Fighter(BLUE)
        p.setPosition(-1000.0, y)
        p.setSpeed(y)
        p.setHeading(0)

        q = Fighter(BLUE)
        q.setPosition(-1000.0, -y)
        q.setSpeed(y)
        q.setHeading(0)

        world.addPlayer(p)
        world.addPlayer(q)


def FireHeadingTest(world):
    p = Fighter(BLUE)
    p.setPosition(x=50, y=0)
    p.setSpeed(0)
    p.setHeading(0)
    p.detectRange = 250
    p.pDetect = 1.0
    p.addSensor(0.25, 750.0, "fighter", 0.75)
    # p.addWeaponLoadout(6,250,250)
    
    p2 = Fighter(RED)
    p2.setPosition(x=150, y=0)
    p2.setSpeed(0)
    p2.setHeading(180)
    p2.detectRange = 250
    p2.pDetect = 1.0
    p2.addSensor(0.25, 750.0, "fighter", 0.75)
    p2.addWeaponLoadout(6,250,250)

    
    world.addPlayer(p)
    world.addPlayer(p2)
    
    
    
    





