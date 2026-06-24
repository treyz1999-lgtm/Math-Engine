
import math



def add(a : float, b : float) -> float:
    return a+b

def subtract(a: float, b : float) -> float:
    return a-b

def multiply(a: float, b : float) -> float:
    return a*b

def divide(a: float, b : float) -> float:
    if b == 0:
        raise ValueError('Cannot divide by zero')
    return a/b

def power(base: float, exponent : int) -> float:
    return math.pow(base, exponent)


def mod(a : float, b : float) -> float: #probably just int
    return a % b



def root(x : float, n: float) -> float: #again probably just int
    return x**(1/n)



def absolute_value(x : float) -> float:
    return abs(x)


def factorial(n : float) -> float:
    if n < 0:
        raise ValueError('Factorial is not defined for negative numbers')
    return math.factorial(n)
