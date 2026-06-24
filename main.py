
import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import geometry_2d as geo_2d
import geometry_3d as geo_3d



#Calculator - make this main file? everything runs on main file
#│
#├── settings
#├── history
#├── menus
#│
#expressions -done
#│   ├── evaluate
#│   ├── derivative
#│   ├── integral
#│   ├── solve
#│   └── limit
#│
#Geometry - done
#│   ├── area
#│   ├── perimeter
#│   └── volume
#│
#│trigonometry -done
#│  │── basic trig
#│  │── inverse trig
#│  │── triangle solvers
#│  └── right triangle helpers
#│
#LinearAlgebra - done
#│   ├── vectors
#│   ├── matrices
#│   └── systems
#│
#Plotter
#│   ├── function graphs
#│   ├── geometry plots
#│   ├── statistical plots
#│   └── vector plots
#│
#Standalone utility functions - done
#   ├── arithmetic
#   └── statistics


#settings
#├── global calculator settings
#└── feature-specific settings
#    └── plot settings

settings = {
    "angle_mode": "degrees",
    "precision": 4,
    "plot": {
        "linewidth": 2,
        "color": "blue",
        "grid": True,
        "points": 500,
        'x_min': -10,
        'x_max': 10,
        "bins": 20,
        "alpha": 0.7,
        'marker': 'o',
        "markersize": 5,

    },
    "calculus": {
        "epsilon": 0.1
    },
}

class Calculator:
    def __init__(self):
        self.history = [] #this will be a list of dictionaries that are structured to match whatever JSON objects we want to pass back from the front end
        self.angle_mode = 'degrees' #by default the calculator will accept angles in degrees. Keep in mind that the math library expects radians so internally all the math is done using radians

    def convert_angle(self, angle):
        if self.angle_mode == 'degrees':
            return math.radians(angle)
        return angle





