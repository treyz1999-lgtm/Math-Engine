
import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import geometry as geom



#Calculator - make this main file? everything runs on main file
#│
#├── settings
#├── history
#├── menus
#│
#Function -this will be a file
#│   ├── evaluate
#│   ├── derivative
#│   ├── integral
#│   ├── solve
#│   └── limit
#│
#Geometry - this will be a file
#│   ├── area
#│   ├── perimeter
#│   └── volume
#│
#LinearAlgebra - this will be a file
#│   ├── vectors
#│   ├── matrices
#│   └── systems
#│
#Plotter - make this a separate file
#│   ├── function graphs
#│   ├── geometry plots
#│   ├── statistical plots
#│   └── vector plots
#│
#Standalone utility functions - incldue in main
#   ├── arithmetic
#    ├── trig
#    └── statistics


#Calculator Class : will hold things like memory, menus, settings, etc

class Calculator:
    def __init__(self):
        self.history = []
        self.angle_mode = 'degrees' #by default the calculator will accept angles in degrees. Keep in mind that the math library expects radians so internally all the math is done using radians

    def convert_angle(self, angle):
        if self.angle_mode == 'degrees':
            return math.radians(angle)
        return angle


    

#Function Class: will hold various functions to calculate expressions

#Geometry Class: will hold all the geometric calculations we might want





#Trigonometry Class: same as geometry but with Trig instead, that might end up as 1 class in the end

#LinearAlgebra Class: will hold the linear algebra functions

#Plotter Class: will hold all the plotting functions

#Conversions Class: this might hold some basic conversions like kg to lbs, etc

#Stand-alone functions: this is where we would put anything that doesn't fall into a class like basic arithmetic and maybe stats



