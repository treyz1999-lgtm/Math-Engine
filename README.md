# Math Engine

A full-stack mathematical computation engine built with **FastAPI**, **Python**, and **vanilla JavaScript** that supports advanced mathematical operations including arithmetic, trigonometry, symbolic algebra, calculus, statistics, geometry, linear algebra, and interactive plotting.

This project was designed to mimic the architecture of a production-style software system rather than a simple calculator. It features a modular backend, dynamic frontend rendering, configurable settings, plotting support, and request history replay.

---

## Features

### Core Math Modules
- Arithmetic operations
- Trigonometry
- Symbolic algebra
- Calculus
- Statistics
- Geometry (2D & 3D)
- Linear algebra
- Plotting / graphing

---

## Supported Operations

### Arithmetic
- Addition
- Subtraction
- Multiplication
- Division
- Modulo
- Roots
- Powers
- Factorials
- Absolute value

---

### Trigonometry
- sin, cos, tan
- sec, csc, cot
- inverse trig functions
- Law of Sines
- Law of Cosines
- Unit circle helpers
- Triangle helpers

Supports:
- Degree mode
- Radian mode

---

### Symbolic Expressions (SymPy)
- Simplify expressions
- Expand expressions
- Factor expressions
- Evaluate expressions
- Solve equations
- Solve systems of equations
- Solve roots

Examples:
```math
(x+2)(x-2)
```

```math
x^2 - 5x + 6 = 0
```

---

### Calculus
- Derivatives
- Higher-order derivatives
- Integrals
- Definite integrals
- Limits
- Domain analysis
- Intercepts
- Critical points
- Local extrema
- Inflection points

Examples:
```math
\frac{d}{dx}(x^3)
```

```math
\int x^2 dx
```

---

### Statistics
- Mean
- Median
- Mode
- Range
- Quartiles
- IQR
- Variance
- Standard deviation
- Percentiles
- Covariance
- Correlation
- Permutations
- Combinations
- Z-score

---

### Geometry 2D
- Square
- Rectangle
- Triangle
- Circle
- Polygon
- Trapezoid
- Parallelogram

Calculates:
- area
- perimeter
- diagonals
- angle sums

---

### Geometry 3D
- Cube
- Sphere
- Cylinder
- Cone
- Pyramid
- Prism

Calculates:
- volume
- surface area
- diagonals
- slant height

---

### Linear Algebra (NumPy)
#### Vector Operations
- Addition
- Subtraction
- Dot product
- Cross product
- Magnitude
- Unit vectors
- Scalar multiplication

#### Matrix Operations
- Addition
- Subtraction
- Multiplication
- Transpose
- Determinant
- Inverse
- Rank
- Trace
- Eigenvalues
- Eigenvectors
- Singular Value Decomposition

#### Linear Systems
Solve:
```math
Ax = b
```

---

### Plotting
Interactive graphs powered by Plotly.

Supports:
- Function plots
- Critical point visualization
- Extrema visualization
- Inflection point visualization
- Histograms
- Box plots
- Scatter plots
- Vector plots

---

# Tech Stack

## Backend
- Python
- FastAPI
- NumPy
- SymPy
- Matplotlib
- Uvicorn
- Pydantic

## Frontend
- HTML
- CSS
- Vanilla JavaScript
- Plotly.js

---

# Architecture

The project follows a modular layered architecture.

```text
Frontend
│
├── index.html
├── styles.css
├── config.js
├── api.js
└── app.js

Backend
│
├── main.py
├── routes/
├── services/
├── utils/
└── state.py
```

---

## Backend Design

### Routes Layer
Responsible for:
- API endpoints
- request validation
- request models
- response formatting

Example:
```python
@router.post("/binary")
```

---

### Services Layer
Responsible for:
- business logic
- mathematical computation
- algorithm execution

Examples:
- arithmetic.py
- trig.py
- expression_engine.py
- stats.py
- linear.py
- plot.py

---

### Utils Layer
Shared helper functions:
- operation resolution
- safe execution
- request logging
- API abstraction

---

### State Management
Global application state stores:
- settings
- history
- replay data

Supports:
- history replay
- configurable plotting
- angle modes
- precision settings

---

# Frontend Design

The frontend behaves like a lightweight single-page application.

Core concepts:
- dynamic form rendering
- event-driven architecture
- client-server communication
- centralized configuration

---

## Config-Driven UI

Rather than hardcoding forms, calculators are generated dynamically from configuration objects.

Example:

```javascript
{
  endpoint: "/trig/basic",
  operations: ["sin", "cos"],
  fields: [...]
}
```

Benefits:
- scalable
- easy to maintain
- reusable UI logic

---

# History System

Every successful calculation is stored in history with:

- endpoint
- request payload
- display name
- output

Example:
```json
{
  "endpoint": "/trig/basic",
  "request": {
    "operation": "sin",
    "value": 45
  }
}
```

This enables:

### Replay
Re-run previous calculations with one click.

### Delete
Remove unwanted history entries.

---

# Settings System

User-adjustable settings include:

## General
- angle mode
- precision

## Plot
- line width
- color
- grid
- point density
- axis range
- histogram bins
- marker size

## Calculus
- epsilon (used for numerical analysis)

---

# Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- REST API design
- FastAPI routing
- Pydantic validation
- Modular architecture
- Separation of concerns
- Error handling
- Dynamic frontend rendering
- State management
- Numerical computing
- Symbolic computation
- Data visualization
- Linear algebra
- Calculus algorithms

---

# Installation

Clone repository:

```bash
git clone https://github.com/treyz1999-lgtm/Math-Engine.git
cd Math-Engine
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn main:app --reload
```

Open browser:

```text
http://127.0.0.1:8000
```

---

# Future Improvements

Potential enhancements:

- React frontend
- Dark mode
- User authentication
- Save history to database
- Export results to CSV/PDF
- Advanced graph controls
- 3D graphing
- Differential equations
- Numerical methods
- Complex analysis tools

