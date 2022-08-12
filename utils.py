import math


def computeSmallestAngleBetweenHeadings(h1, h2):

    radiansH1 = math.radians(h1)
    radiansH2 = math.radians(h2)

    a = (radiansH1 - radiansH2) % (2 * math.pi)
    b = (radiansH2 - radiansH1) % (2 * math.pi)

    if a < b:
        return math.degrees(-a)
    else:
        return math.degrees(b)


def computeDistance(x1, y1, x2, y2):
    """
    The standard distance formula.
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def computeHeading(x1, y1, x2, y2):
    # 0 is west, 90 is north
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def normalize2dVector(v):
    vLength = math.hypot(float(v[0]), float(v[1]))
    if vLength == 0:
        return [0, 0]
    return [float(v[0]) / vLength, float(v[1]) / vLength]


def normalizeAngle(angle):
    result = angle
    while result < 0:
        result += 360
    while result > 360:
        result -= 360
    return result


def computeRangeToTarget(me, target):
    return computeDistance(me.x, me.y, target.x, target.y)


def projectPoint(x, y, hdg, distance):
    x2 = x + distance * math.cos(math.radians(hdg))
    y2 = y + distance * math.sin(math.radians(hdg))
    return x2, y2


def tx_world_to_screen(x, y, world, screen_size) -> tuple:
    world_dx = world.maxX - world.minX
    world_dy = world.maxY - world.minY
    tx = ((x - world.minX) / world_dx) * screen_size[0]
    ty = screen_size[1] - ((y - world.minY) / world_dy) * screen_size[1]
    return tx, ty
