import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
from services.expression_engine import (to_sympy, critical_points, local_extrema, inflection_points)
from services.stats import (to_array, validate_array)


#plot.py
#├── plot_function() - done
#├── plot_shape()
#├── plot_histogram()
#├── plot_scatter()
#└── plot_vectors()


#├── plot_function()              # base plot
#├── plot_critical_points()       # variant
#├── plot_extrema()               # variant
#└── plot_inflection_points()     # variant

def _build_function_plot(expr: str, variable: str, plot_settings: dict):
    """
    Build a Matplotlib plot for a single-variable mathematical function.

    This is an internal helper function used by all public plotting functions.
    It handles the common plotting workflow:
        1. Parse and validate the mathematical expression
        2. Generate x-values over the specified domain
        3. Evaluate the function numerically using NumPy
        4. Filter out invalid values (inf, -inf, nan)
        5. Draw the function and graph formatting

    This function intentionally does NOT call plt.show().
    Public plotting functions (such as plot_function(),
    plot_critical_points(), and plot_extrema()) are responsible
    for displaying the final graph after adding any overlays.

    Args:
        expr (str):
            Mathematical expression entered by the user.

            Examples:
                "x^2"
                "sin(x)"
                "1/x"

        variable (str):
            Independent variable used in the expression.

            Example:
                "x"

        plot_settings (dict):
            Dictionary containing plot configuration.

            Required keys:
                linewidth (int | float)
                color (str)
                grid (bool)
                points (int)
                x_min (int | float)
                x_max (int | float)

    Raises:
        ValueError:
            If plot settings are invalid or the function
            cannot be evaluated over the specified range.
    """
    linewidth = plot_settings["linewidth"]
    color = plot_settings["color"]
    grid = plot_settings["grid"]
    points = plot_settings["points"]
    x_min = plot_settings["x_min"]
    x_max = plot_settings["x_max"]


    symbol = sy.Symbol(variable)
    expression = to_sympy(expr)

    # Validate plot range
    if x_min >= x_max:
        raise ValueError("x_min must be less than x_max")

    # Need at least two points to draw a line
    if points < 2:
        raise ValueError("points must be at least 2")

    # Ensure chosen variable exists in expression
    # Constants (ex: "5") are still allowed
    if expression.free_symbols and symbol not in expression.free_symbols:
        raise ValueError(
            f"Expression does not contain variable '{variable}'"
        )

    x_values = np.linspace(x_min, x_max, points)

    function = sy.lambdify(symbol, expression, "numpy")

    try:
        y_values = function(x_values)
    except Exception:
        raise ValueError(
            "Function could not be evaluated in the given range"
        )

    # Handle constant functions (ex: y = 5)
    if np.isscalar(y_values):
        y_values = np.full_like(x_values, y_values, dtype=float)

    # Remove invalid values such as inf, -inf, and nan
    mask = np.isfinite(y_values)
    x_values = x_values[mask]
    y_values = y_values[mask]

    plt.figure()

    plt.plot(
        x_values,
        y_values,
        color=color,
        linewidth=linewidth
    )

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)

    plt.xlabel(variable)
    plt.ylabel("f(x)")
    plt.title(f"f({variable}) = {expr}")

    if grid:
        plt.grid()


def plot_function(expr: str, variable: str, plot_settings: dict):
   _build_function_plot(expr, variable, plot_settings)
   plt.show()

def plot_critical_points(expr: str, variable: str, plot_settings: dict):
    _build_function_plot(expr, variable, plot_settings)
    points = critical_points(expr, variable)

    for x,y in points:
        plt.scatter(float(x), float(y))

def plot_extrema(expr: str, variable: str, plot_settings: dict):
    _build_function_plot(expr, variable, plot_settings)
    extrema = local_extrema(expr, variable)

    for x, y, classification in extrema:
        plt.scatter(float(x), float(y))
        plt.annotate(classification, (float(x), float(y)))

    plt.show()

def plot_inflections(expr: str, variable: str, settings : dict):
    epsilon = settings['calculus']['epsilon']

    _build_function_plot(expr, variable, settings['plot'])

    points = inflection_points(expr, variable, epsilon)

    if not points:
        print("No inflection points found in the function.")

    for x,y in points:
        plt.scatter(float(x), float(y))

    plt.show()

# Statistical plots
# ├── histogram
# ├── boxplot
# └── scatter

def plot_histogram(data , settings : dict):
    """
       Plot a histogram for a numeric dataset.

       A histogram groups numeric values into bins and displays the
       frequency of values within each bin. This is useful for
       visualizing the distribution of data, including spread,
       skewness, clustering, and potential outliers.

       This function:
       1. Validates that the input data is non-empty and iterable
       2. Converts the data into a NumPy array of floats
       3. Retrieves histogram settings such as color and bin count
       4. Validates that the number of bins is a positive integer
       5. Plots and displays the histogram using matplotlib

       Examples:
           data = [1, 2, 2, 3, 4, 5, 5, 5, 8]

           Possible histogram interpretation:
               Bin 1: 1–2   -> 3 values
               Bin 2: 3–4   -> 2 values
               Bin 3: 5–6   -> 3 values
               Bin 4: 7–8   -> 1 value

       Args:
           data:
               Iterable collection of numeric values.

               Examples:
                   [1, 2, 3, 4]
                   (10, 12, 15)
                   np.array([5, 6, 7])

           settings (dict):
               Calculator settings dictionary containing plot settings.

               Required keys:
                   settings["plot"]["color"]
                   settings["plot"]["bins"]

       Returns:
           None

           Displays a histogram plot using matplotlib.

       Raises:
           ValueError:
               Raised if:
                   - data is empty
                   - data is not iterable
                   - data contains non-numeric values
                   - bins is not an integer
                   - bins is less than 1
       """
    validate_array(data)
    data = to_array(data)
    color = settings['plot']['color']
    bins = settings['plot']['bins']
    if not isinstance(bins, int):
        raise ValueError("bins must be an integer")

    if bins < 1:
        raise ValueError("bins must be at least 1")

    plt.hist(data, bins=bins, color=color)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Basic Histogram')
    plt.show()

def plot_boxplot(data):
    validate_array(data)
    data = to_array(data)

    plt.boxplot(data)
    plt.ylabel("Values")
    plt.title("Box Plot")
    plt.show()

def plot_scatterplot(x_data: list, y_data: list, settings: dict):

    color = settings["plot"]["color"]
    alpha = settings["plot"]["alpha"]
    grid = settings["plot"]["grid"]
    marker = settings["plot"]["marker"]
    markersize = settings["plot"]["markersize"]

    validate_array(x_data)
    validate_array(y_data)

    if len(x_data) != len(y_data):
        raise ValueError("x_data and y_data must have same length")

    x_data = to_array(x_data)
    y_data = to_array(y_data)

    plt.scatter(
        x_data,
        y_data,
        color=color,
        alpha=alpha,
        marker=marker,
        s=markersize
    )

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scatter Plot")

    if grid:
        plt.grid()

    plt.show()

def plot_vectors(vector_list: list, settings: dict):
    """
    Plot 2D vectors from the origin.

    Args:
        vector_list:
            List of coordinate pairs representing vectors.

            Example:
                [(3, 4), (1, 2), (-2, 5)]

        settings:
            Calculator settings dictionary containing plot settings.
    """
    color = settings["plot"]["color"]

    for vector in vector_list:
        if len(vector) != 2:
            raise ValueError(
                "Each vector must contain exactly 2 coordinates (x, y)"
            )

        x = float(vector[0])
        y = float(vector[1])

        plt.quiver(0, 0, x, y, color=color)

    plt.axhline(0)
    plt.axvline(0)
    plt.gca().set_aspect("equal")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Vector Plot")

    plt.show()

"""
if __name__ == "__main__": #this is for testing purposes
    test_settings = {
        "linewidth": 2,
        "color": "blue",
        "grid": True,
        "points": 500,
        "x_min": -10,
        "x_max": 10
    }





plot_extrema("x^3-3x", "x", test_settings)

"""

#Future feature:
#- optional geometry visualization
#- more linear algebra plots or system of equations plotting