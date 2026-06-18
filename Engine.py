# I will eventual build out a calculator program with various functionality and it will have some sort of GUI that allows the user to select whatever calculations they want. I will need to build out some classes over time and their methods will be the differenct calculations

import math

radius = float(input("Enter the radius of the circle: "))

circumference = 2 * math.pi * radius
print(f' The circumference of the circle is: {circumference}')

area = math.pi * pow(radius, 2)
print(f'The area of the circle is: {area}')


class Rectangle:  # we will make a class called Rectangle to represent the rectangle and its properties (width and height/length) and it will have a method called area to calculate the area of the rectangle.
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# get user input for width and height of the rectangle
print(
    "This will calculate the area of a rectangle. Please enter the width and height of the rectangle. Where height and length are the same thing")
width = float(input(
    "What is the width of the rectangle?:  "))  # type cast the user input to a float so we can do calculations with it
length = float(input("What is the length of the rectangle?: "))

# Create an instance of the Rectangle class with the user input
new_rectangle = Rectangle(width, length)
new_rectangle.area()  # call the area method to calculate the area of the rectangle and print it out
print(f"The area of the rectangle is: {new_rectangle.area()}")


# find hypotenuse of a right triangle using the Pythagorean theorem
class RightTriangle:
    def __init__(self, side_a, side_b):
        self.side_a = float(side_a)
        self.side_b = float(side_b)

    def hypotenuse(self):
        return math.sqrt(pow(self.side_a, 2) + pow(self.side_b, 2))


print(
    "This will calculate the hypotenuse of a right triangle using the Pythagorean theorem. Please enter the lengths of the two sides of the triangle.")
side_a = input('Enter the length of side 1: ')
side_b = input('Enter the length of side 2: ')
new_triangle = RightTriangle(side_a, side_b)
print(f'The length of the hypotenuse is: {new_triangle.hypotenuse()}')

# maybe we can make an arthemtic class that will have all the basic arthemtic operations (addition, subtraction, multiplication, division) and then we can make a loop that will ask the user which operation they want to perform and then it will ask for the numbers and then it will perform the operation and print the result. We can also add some error handling for division by zero and invalid input. How would we handle more than 2 numbers for the operations? It would also be nice is the user could just input a string like "2 + 2" and then we could parse the string and perform the operation. That would be a nice feature to have. We could also add some more advanced operations like exponentiation and square root. We could also add some trigonometric functions like sine, cosine, and tangent.
# so then really i should make a parser to start that will take the string and figure out what operations the user is using and then what class it needs

# we will also have some conversions in here as well like converting between different units of measurement (inches to centimeters, pounds to kilograms, etc.)

weight = float(input('Enter your weight: '))
unit = input(' Kilograms or Pounds? (type "kg" for kilograms and "lb" for pounds): ')
# we also will round to 2 decimal places for the output of the conversions
if unit.lower() == 'kg':
    weight = round(weight * 2.20462, 2)
    print(f'Your weight in pounds is: {weight} lbs')
elif unit.lower() == 'lb':
    weight = round(weight * 0.453592, 2)
    print(f'Your weight in kilograms is: {weight} kgs')
else:
    print('Invalid input. Please enter "kg" for kilograms or "lb" for pounds.')

# we can have a variety of conversions available that i build out later
unit = input(
    'What unit is this temperature in? (type "C" for Celsius and "F" for Fahrenheit): ')  # i will add kelvin later as well
temperature = float(input('Enter the temperature: '))
if unit.lower() == 'c' or unit.lower() == 'celsius':
    temperature = round((temperature * 9 / 5) + 32, 2)
    print(f'The temperature in Fahrenheit is: {temperature} °F')
elif unit.lower() == 'f' or unit.lower() == 'fahrenheit':
    temperature = round((temperature - 32) * 5 / 9, 2)
    print(f'The temperature in Celsius is: {temperature} °C')
else:
    print('Invalid input. Please enter "C" for Celsius or "F" for Fahrenheit.')

# we will also have a compound interest calculator that will calculate the future value of an investment based on the principal amount, interest rate, and number of years. We can also add an option for monthly contributions to the investment as well.
# i will start with a basic concept

principal = float(input('Enter the principal amount: '))
rate = float(input('Enter the annual interest rate (as a percentage as a whole number): ')) / 100
years = int(input('Enter the number of years: '))

final_amount = round(principal * pow((1 + rate), years),
                     2)  # this is the formula for compound interest without monthly contributions
print(f'The future value of the investment is: ${final_amount}')
# also need a flag for when the user enters principle as anything that is less than or equal to 0

# we can start building some of the classes for the fucations we will use now, starting with a divsion class

# we will now build a division class