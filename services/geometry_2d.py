import math

# Squares
def square_area(side):
    if side <= 0:
        raise ValueError("Side must be greater than 0")
    return side ** 2


def square_perimeter(side):
    if side <= 0:
        raise ValueError("Side must be greater than 0")
    return side * 4


def square_diagonal(side):
    if side <= 0:
        raise ValueError("Side must be greater than 0")
    return side * math.sqrt(2)


# Rectangles
def rectangle_area(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Sides must be greater than 0")
    return a * b


def rectangle_perimeter(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Sides must be greater than 0")
    return 2 * (a + b)


def rectangle_diagonal(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Sides must be greater than 0")
    return math.sqrt(a**2 + b**2)


# Triangles
def triangle_area_right(base, height):
    if base <= 0 or height <= 0:
        raise ValueError("Inputs must be greater than 0")
    return 0.5 * base * height


def triangle_area_equilateral(a):
    if a <= 0:
        raise ValueError("Side must be greater than 0")
    return (math.sqrt(3) / 4) * a**2


def triangle_area_isosceles(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Inputs must be greater than 0")
    if 2 * a <= b:
        raise ValueError("Invalid triangle")
    return (b / 4) * math.sqrt(4 * a**2 - b**2)


def triangle_area_sss(a, b, c):
    if any(side <= 0 for side in (a, b, c)):
        raise ValueError("Sides must be greater than 0")
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Invalid triangle")

    s = (a + b + c) / 2
    return math.sqrt(s * (s-a) * (s-b) * (s-c))


def triangle_perimeter(a, b, c):
    if any(side <= 0 for side in (a, b, c)):
        raise ValueError("Sides must be greater than 0")
    return a + b + c


# Circles
def circle_area(radius):
    if radius <= 0:
        raise ValueError("Radius must be greater than 0")
    return math.pi * radius**2


def circle_circumference(radius):
    if radius <= 0:
        raise ValueError("Radius must be greater than 0")
    return 2 * math.pi * radius


# Parallelograms
def parallelogram_area(base, height):
    return base * height


def parallelogram_perimeter(a, b):
    return 2 * (a + b)


# Trapezoids
def trapezoid_area(b1, b2, h):
    return ((b1 + b2) * h) / 2


def trapezoid_perimeter(a, b, c, d):
    return a + b + c + d


# Regular Polygons
def regular_polygon_area(n, s):
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides")
    return (n * s**2) / (4 * math.tan(math.pi / n))


def regular_polygon_perimeter(n, s):
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides")
    return n * s


def polygon_interior_angle_sum(n):
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides")
    return (n - 2) * 180


def regular_polygon_interior_angle(n):
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides")
    return ((n - 2) * 180) / n