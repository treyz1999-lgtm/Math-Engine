#this will contain the geometry class and all its associated functions
import math

##likely do not need to use __name__ == __main__ if this file just contains our methods

#squares
def square_area(side):
    if side < 0: #this would be better as <= but if someone inputs 0 for this then... they aren't really thinking much... we will just return 0
        raise ValueError('side(s) cannot be negative')
    return side**2


def square_perimeter(side):
    if side < 0:
        raise ValueError('side(s) cannot be negative') #technically we could accept negatives here, but it just wouldn't translate to anything meaningful in the real world
    return side * 4


def diagonal_square(side):
    if side < 0:
        raise ValueError('side(s) cannot be negative')
    return side * math.sqrt(2)

#rectangles

def rectangle_area(side_a, side_b):
    if side_a < 0 or side_b < 0:
        raise ValueError('side(s) cannot be negative')
    return side_a * side_b


def rectangle_perimeter(side_a, side_b):
    if side_a < 0 or side_b < 0:
        raise ValueError('side(s) cannot be negative')
    return 2*(side_a + side_b)


def diagonal_rectangle(side_a, side_b):
    if side_a < 0 or side_b < 0:
        raise ValueError('side(s) cannot be negative')
    return math.sqrt(side_a**2 + side_b**2)

#triangles

def right_triangle_area(base, height):
    if base < 0 or height < 0:
        raise ValueError('side(s) cannot be negative')
    return 0.5 * base * height


def equilateral_triangle_area(a):
        if a <= 0:
            raise ValueError("Side(s) length must be greater than 0")
        return (math.sqrt(3) / 4) * a ** 2


def isosceles_triangle_area(a, b):
    if a < 0 or b < 0:
        raise ValueError('side(s) length must be greater than 0')
    if 2 * a <= b:
        raise ValueError("Invalid isosceles triangle")
    return b/4*math.sqrt(4*a**2 - b**2)



def triangle_area_sss(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Invalid triangle")
    if any(side <= 0 for side in (a, b, c)):
        raise ValueError("Side(s) length must be greater than 0")
    s = (a + b + c) / 2
    return math.sqrt((s*(s - a)*(s - b)*(s - c)))


def triangle_area_sas(side1, side2, angle, calculator):
    angle = calculator.convert_angle(angle)

    if angle <= 0 or angle >= math.pi:
        raise ValueError("Invalid angle")

    return 0.5 * side1 * side2 * math.sin(angle)


def perimeter_sss(a, b, c):
    if any(side <=0 for side in (a, b, c)):
        raise ValueError("Side(s) length must be greater than 0")
    return a + b + c

    #circles

def circle_area(radius):
    return math.pi * radius**2


def circumference(radius):
    return 2 * math.pi * radius


def arc_length(r, angle, calculator):
    angle = calculator.convert_angle(angle)
    return r*angle

    #parallelograms


def parallelogram_area_bh(base, height):
    return base * height


def parallelogram_area_sin(length, angle, calculator):
    angle = calculator.convert_angle(angle)
    return length**2*math.sin(angle)


def parallelogram_area_diagonals(d1, d2, angle, calculator):
    angle = calculator.convert_angle(angle)
    return (d1 * d2*math.sin(angle))/2


def parallelogram_perimeter(a, b):
    return 2*(a+b)

    #trapezoid

def trapezoid_area(b1, b2, h):
    return ((b1 + b2)*h)/2


def trapezoid_perimeter(a, b, c, d): #this is the same as rectangle perimeter
    return a + b + c + d

#polygons

def polygon_area(n, s): # we can handle regular polygons, but we would need a more robust function for irregular polygons
     return (n * s**2)/(4*math.tan(math.pi/n))

def regular_polygon_perimeter(n, s):
    return n*s


def interior_angle_sum_polygon(n):
    if n < 3:
        raise ValueError("A polygon must have at least 3 sides")

    return (n - 2) * 180

def polygon_interior_angle(n):
    if n < 3:
        raise ValueError("A polygon must have at least 3 sides")

    return ((n - 2) * 180) / n

#cube
def volume_cube(s):
    return s**3

def surface_area_cube(s):
    return 6*s**2

def perimeter_cube(s):
    return 12*s

#rectangular prism
def volume_prism( l, w, h):
    return l*w*h

def area_prism( l, w, h):
    return 2*((w*l)+(h*l)+(h*w))

def diagonal_prism( l, w, h):
    return math.sqrt(l**2 + w**2 + h**2)


