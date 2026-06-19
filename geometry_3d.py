import math

# Cube
def cube_volume(s):
    if s <= 0:
        raise ValueError("Side must be greater than 0")
    return s**3


def cube_surface_area(s):
    if s <= 0:
        raise ValueError("Side must be greater than 0")
    return 6 * s**2


def cube_edge_sum(s):
    if s <= 0:
        raise ValueError("Side must be greater than 0")
    return 12 * s


# Rectangular Prism
def prism_volume(l, w, h):
    if l <= 0 or w <= 0 or h <= 0:
        raise ValueError("Inputs must be greater than 0")
    return l * w * h


def prism_surface_area(l, w, h):
    if l <= 0 or w <= 0 or h <= 0:
        raise ValueError("Inputs must be greater than 0")
    return 2 * ((l*w) + (l*h) + (w*h))


def prism_diagonal(l, w, h):
    if l <= 0 or w <= 0 or h <= 0:
        raise ValueError("Inputs must be greater than 0")
    return math.sqrt(l**2 + w**2 + h**2)


# Sphere
def sphere_volume(radius):
    if radius <= 0:
        raise ValueError("Radius must be greater than 0")
    return (4 / 3) * math.pi * radius**3


def sphere_surface_area(radius):
    if radius <= 0:
        raise ValueError("Radius must be greater than 0")
    return 4 * math.pi * radius**2


# Cylinder
def cylinder_volume(radius, height):
    if radius <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return math.pi * radius**2 * height


def cylinder_surface_area(radius, height):
    if radius <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return (2 * math.pi * radius * height) + (2 * math.pi * radius**2)


# Cone
def cone_slant_height(radius, height):
    if radius <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return math.sqrt(radius**2 + height**2)


def cone_volume(radius, height):
    if radius <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return (1 / 3) * math.pi * radius**2 * height


def cone_surface_area(radius, height):
    if radius <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")

    l = cone_slant_height(radius, height)
    return math.pi * radius * (radius + l)


# Pyramid
def pyramid_volume(base_area, height):
    if base_area <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return (1 / 3) * base_area * height