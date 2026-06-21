
import math



def add(a, b):
    return a+b

def subtract(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    if b == 0:
        raise ValueError('Cannot divide by zero')
    return a/b

def power(base, exponent):
    return math.pow(base, exponent)


def mod(a, b):
    return a % b



def root(x, n):
    return x**(1/n)



def absolute_value(x):
    return abs(x)


def factorial(n):
    if n < 0:
        raise ValueError('Factorial is not defined for negative numbers')
    return math.factorial(n)
    return math.factorial(n)