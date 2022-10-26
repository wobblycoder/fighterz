import math


def find_angle_between_headings(h1, h2):

    hdg1_rad = math.radians(h1)
    hdg2_rad = math.radians(h2)

    a = (hdg1_rad - hdg2_rad) % (2 * math.pi)
    b = (hdg2_rad - hdg1_rad) % (2 * math.pi)

    if a < b:
        return math.degrees(-a)
    else:
        return math.degrees(b)


def compute_distance(x1, y1, x2, y2):

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def heading_between_points(x1, y1, x2, y2):
    # 0 is west, 90 is north
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def normalize_2d_vector(v):
    vLength = math.hypot(float(v[0]), float(v[1]))
    if vLength == 0:
        return [0, 0]
    return [float(v[0]) / vLength, float(v[1]) / vLength]


def normalize_angle(angle):
    result = angle
    while result < 0:
        result += 360
    while result > 360:
        result -= 360
    return result


def range_to_tgt(me, target):
    return compute_distance(me.x, me.y, target.x, target.y)


def project_point(x, y, hdg, distance):
    x2 = x + distance * math.cos(math.radians(hdg))
    y2 = y + distance * math.sin(math.radians(hdg))
    return x2, y2


def tx_world_to_screen(x, y, world, screen_size) -> tuple:
    world_dx = world.maxX - world.minX
    world_dy = world.maxY - world.minY
    tx = ((x - world.minX) / world_dx) * screen_size[0]
    ty = screen_size[1] - ((y - world.minY) / world_dy) * screen_size[1]
    return tx, ty
