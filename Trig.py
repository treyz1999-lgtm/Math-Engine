import math

#basic functions

#inverse functions

#triangle solvers

#triangle helpers

#unit circle helpers


def trig_sin(angle, calculator):
    angle = calculator.convert_angle(angle)
    return math.sin(angle)


def trig_cos(angle, calculator):
    angle = calculator.convert_angle(angle)
    return math.cos(angle)


def trig_tan(angle, calculator):
    angle = calculator.convert_angle(angle)
    return math.tan(angle)


def trig_sec(angle, calculator):
    angle = calculator.convert_angle(angle)
    cos_val = math.cos(angle)

    if abs(cos_val) < 1e-12:
        raise ValueError("sec undefined for this angle")

    return 1 / cos_val


def trig_csc(angle, calculator):
    angle = calculator.convert_angle(angle)
    sin_val = math.sin(angle)

    if abs(sin_val) < 1e-12:
        raise ValueError("csc undefined for this angle")

    return 1 / sin_val


def trig_cot(angle, calculator):
    angle = calculator.convert_angle(angle)
    tan_val = math.tan(angle)

    if abs(tan_val) < 1e-12:
        raise ValueError("cot undefined for this angle")

    return 1 / tan_val



# INVERSE TRIG FUNCTIONS


def trig_arcsin(value, calculator):
    if value < -1 or value > 1:
        raise ValueError("Input must be between -1 and 1")

    angle = math.asin(value)

    if calculator.angle_mode == 'degrees':
        return math.degrees(angle)

    return angle


def trig_arccos(value, calculator):
    if value < -1 or value > 1:
        raise ValueError("Input must be between -1 and 1")

    angle = math.acos(value)

    if calculator.angle_mode == 'degrees':
        return math.degrees(angle)

    return angle


def trig_arctan(value, calculator):
    angle = math.atan(value)

    if calculator.angle_mode == 'degrees':
        return math.degrees(angle)

    return angle



# TRIANGLE SOLVERS


def triangle_side_law_of_sines(known_side, known_angle, target_angle, calculator):
    if known_side <= 0:
        raise ValueError("Side must be greater than 0")

    known_angle = calculator.convert_angle(known_angle)
    target_angle = calculator.convert_angle(target_angle)

    return known_side * math.sin(target_angle) / math.sin(known_angle)


def triangle_angle_law_of_sines(known_side, known_angle, target_side, calculator):
    if known_side <= 0 or target_side <= 0:
        raise ValueError("Sides must be greater than 0")

    known_angle = calculator.convert_angle(known_angle)

    value = (target_side * math.sin(known_angle)) / known_side

    if value < -1 or value > 1:
        raise ValueError("No valid triangle exists")

    angle = math.asin(value)

    if calculator.angle_mode == 'degrees':
        return math.degrees(angle)

    return angle


def triangle_side_law_of_cosines(side1, side2, included_angle, calculator):
    if side1 <= 0 or side2 <= 0:
        raise ValueError("Sides must be greater than 0")

    angle = calculator.convert_angle(included_angle)

    return math.sqrt(
        side1**2 + side2**2 - 2 * side1 * side2 * math.cos(angle)
    )


def triangle_angle_law_of_cosines(a, b, c, calculator):
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("Sides must be greater than 0")

    numerator = a**2 + b**2 - c**2
    denominator = 2 * a * b

    value = numerator / denominator

    if value < -1 or value > 1:
        raise ValueError("Invalid triangle")

    angle = math.acos(value)

    if calculator.angle_mode == 'degrees':
        return math.degrees(angle)

    return angle



# TRIANGLE HELPERS


def triangle_hypotenuse(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Sides must be greater than 0")

    return math.sqrt(a**2 + b**2)


def triangle_leg(hypotenuse, leg):
    if hypotenuse <= 0 or leg <= 0:
        raise ValueError("Sides must be greater than 0")

    if leg >= hypotenuse:
        raise ValueError("Hypotenuse must be longest side")

    return math.sqrt(hypotenuse**2 - leg**2)


def triangle_third_angle(angle1, angle2, calculator):
    if calculator.angle_mode == 'degrees':
        if angle1 <= 0 or angle2 <= 0:
            raise ValueError("Angles must be positive")
        if angle1 + angle2 >= 180:
            raise ValueError("Invalid triangle")
        return 180 - angle1 - angle2

    else:
        if angle1 <= 0 or angle2 <= 0:
            raise ValueError("Angles must be positive")
        if angle1 + angle2 >= math.pi:
            raise ValueError("Invalid triangle")
        return math.pi - angle1 - angle2



# UNIT CIRCLE HELPERS


def unit_circle_coordinates(angle, calculator):
    angle = calculator.convert_angle(angle)
    x = math.cos(angle)
    y = math.sin(angle)
    return (x, y)


def unit_circle_quadrant(angle, calculator):
    angle = calculator.convert_angle(angle)

    angle = angle % (2 * math.pi)

    if 0 < angle < math.pi / 2:
        return 1
    elif math.pi / 2 < angle < math.pi:
        return 2
    elif math.pi < angle < 3 * math.pi / 2:
        return 3
    elif 3 * math.pi / 2 < angle < 2 * math.pi:
        return 4
    else:
        return "On Axis"