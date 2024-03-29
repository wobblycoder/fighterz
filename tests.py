from typing import List
from fighter import Fighter
from colors import BLUE, RED


def heading_test() -> List[Fighter]:
    """
    show enemy players in a ring around a friendly
    """
    players = []
    x = -900
    for h in range(0, 360, 15):
        p = Fighter(BLUE)
        p.setPosition(x=x, y=0)
        p.setSpeed(200)
        p.setHeading(h)
        p.detectRange = 250
        p.pDetect = 0.5
        x += 64
        players.append(p)
        return players


def one_on_one_pursuit() -> List[Fighter]:
    """
    a 1v1 chase test
    """
    players = []
    p = Fighter(BLUE)
    p.setPosition(-900.0, 0)
    p.setSpeed(100)
    p.setHeading(0)
    p.addSensor(1.0, 600.0, "fighter", 1.0)
    # p.addWeaponLoadout(1, 500, 120)

    q = Fighter(RED)
    q.setPosition(900, 0)
    q.setHeading(180)
    q.setSpeed(100)
    q.addSensor(1.5, 400.0, "fighter", 0.75)

    players.append(p)
    players.append(q)

    return players


def speed_test() -> List[Fighter]:

    players = []

    for y in range(700):
        p = Fighter(BLUE)
        p.setPosition(-1000.0, y)
        p.setSpeed(y)
        p.setHeading(0)

        q = Fighter(BLUE)
        q.setPosition(-1000.0, -y)
        q.setSpeed(y)
        q.setHeading(0)

        players.append(p)
        players.append(q)

    return players


def fire_heading_test() -> List[Fighter]:

    players = []

    p = Fighter(BLUE)
    p.setPosition(x=50, y=0)
    p.setSpeed(0)
    p.setHeading(0)
    p.detectRange = 250
    p.pDetect = 1.0
    p.addSensor(0.25, 750.0, "fighter", 0.75)
    # p.addWeaponLoadout(6,250,250)

    q = Fighter(RED)
    q.setPosition(x=250, y=0)
    q.setSpeed(1)
    q.setHeading(180)
    q.detectRange = 250
    q.pDetect = 1.0
    q.addSensor(0.25, 750.0, "fighter", 0.75)
    q.addWeaponLoadout(6, 250, 250)

    players.append(p)
    players.append(q)

    return players
