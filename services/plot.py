import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
from services.expression_engine import (to_sympy, critical_points, local_extrema, inflection_points)
from services.stats import (to_array, validate_array)
from utils.plot_helpers import (create_figure, apply_plot_settings, build_plot_response)


"""
Plot Response Architecture
--------------------------

Plot endpoints return BOTH structured plot data and a rendered PNG image.

Why return both?
    The calculator frontend is intended to render interactive plots using
    JavaScript charting libraries (such as Plotly, Chart.js, D3, etc.).
    These libraries typically expect raw coordinate or dataset values
    rather than pre-rendered images.

    Example line plot data:
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        }

    Using raw plot data allows the frontend to:
        - render interactive charts
        - zoom and pan
        - show tooltips
        - support hover interactions
        - restyle plots without recomputing math

Why also return a PNG?
    The backend still generates a matplotlib plot and encodes it as a PNG
    image. This acts as a fallback if frontend rendering fails or if a
    plot type is not yet implemented in JavaScript.

Response structure:
    Every plot service returns a standardized dictionary:

        {
            "plot_type": str,
            "plot_data": dict,
            "png": str
        }

Fields:
    plot_type:
        Tells the frontend what type of renderer to use.

        Examples:
            "line"
            "scatter"
            "histogram"
            "boxplot"
            "vector"

    plot_data:
        Contains raw numeric data and optional metadata needed for
        frontend rendering.

        Examples:
            Line plot:
                {
                    "x": [...],
                    "y": [...]
                }

            Histogram:
                {
                    "data": [...],
                    "bins": 20
                }

    png:
        Base64-encoded PNG image of the matplotlib figure.

Important:
    The exact JSON key names are not required by JavaScript itself.
    They are part of the API contract defined by this backend.

    The frontend code simply agrees to expect this structure.

Example frontend flow:
    response = API call

    if response["plot_data"] exists:
        render interactive plot using JS
    else:
        display response["png"]

In short:
    Backend computes math + produces fallback image.
    Frontend prefers raw plot data for interactive visualization.
"""

def _build_function_plot(expr: str, variable: str, settings: dict):
    """
    Build a function plot and return computed plot data.
    """
    plot_settings = settings["plot"]

    linewidth = plot_settings["linewidth"]
    color = plot_settings["color"]
    points = plot_settings["points"]
    x_min = plot_settings["x_min"]
    x_max = plot_settings["x_max"]

    symbol = sy.Symbol(variable)
    expression = to_sympy(expr)

    if x_min >= x_max:
        raise ValueError("x_min must be less than x_max")

    if points < 2:
        raise ValueError("points must be at least 2")

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

    if np.isscalar(y_values):
        y_values = np.full_like(x_values, y_values, dtype=float)

    mask = np.isfinite(y_values)
    x_values = x_values[mask]
    y_values = y_values[mask]

    create_figure()

    plt.plot(
        x_values,
        y_values,
        color=color,
        linewidth=linewidth
    )

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)

    apply_plot_settings(
        title=f"f({variable}) = {expr}",
        x_label=variable,
        y_label="f(x)",
        settings=settings
    )

    return x_values, y_values

def plot_function(expr: str, variable: str, settings: dict):
    x_values, y_values = _build_function_plot(
        expr,
        variable,
        settings
    )

    return build_plot_response(
        "line",
        {
            "x": x_values,
            "y": y_values,
            "expression": expr,
            "variable": variable
        }
    )

def plot_critical_points(expr: str, variable: str, settings: dict):
    x_values, y_values = _build_function_plot(
        expr,
        variable,
        settings
    )

    points = critical_points(expr, variable)

    critical_x = []
    critical_y = []

    for x, y in points:
        x = float(x)
        y = float(y)

        critical_x.append(x)
        critical_y.append(y)

        plt.scatter(x, y)

    return build_plot_response(
        "line",
        {
            "x": x_values,
            "y": y_values,
            "critical_x": critical_x,
            "critical_y": critical_y
        }
    )

def plot_extrema(expr: str, variable: str, settings: dict):
    x_values, y_values = _build_function_plot(
        expr,
        variable,
        settings
    )

    extrema = local_extrema(expr, variable)
    extrema_data = []

    for x, y, classification in extrema:
        x = float(x)
        y = float(y)

        plt.scatter(x, y)
        plt.annotate(classification, (x, y))

        extrema_data.append({
            "x": x,
            "y": y,
            "classification": classification
        })

    return build_plot_response(
        "line",
        {
            "x": x_values,
            "y": y_values,
            "extrema": extrema_data
        }
    )

def plot_inflections(expr: str, variable: str, settings: dict):
    epsilon = settings["calculus"]["epsilon"]

    x_values, y_values = _build_function_plot(
        expr,
        variable,
        settings
    )

    points = inflection_points(expr, variable, epsilon)
    inflection_data = []

    for x, y in points:
        x = float(x)
        y = float(y)

        plt.scatter(x, y)

        inflection_data.append({
            "x": x,
            "y": y
        })

    return build_plot_response(
        "line",
        {
            "x": x_values,
            "y": y_values,
            "inflections": inflection_data
        }
    )

def plot_histogram(data, settings: dict):
    validate_array(data)
    data = to_array(data)

    color = settings["plot"]["color"]
    bins = settings["plot"]["bins"]

    if bins < 1:
        raise ValueError("bins must be at least 1")

    create_figure()

    plt.hist(data, bins=bins, color=color)

    apply_plot_settings(
        title="Histogram",
        x_label="Values",
        y_label="Frequency",
        settings=settings
    )

    return build_plot_response(
        "histogram",
        {
            "data": data,
            "bins": bins
        }
    )

def plot_boxplot(data, settings=None):
    validate_array(data)
    data = to_array(data)

    create_figure()
    plt.boxplot(data)

    plt.ylabel("Values")
    plt.title("Box Plot")

    return build_plot_response(
        "boxplot",
        {
            "data": data
        }
    )

def plot_scatterplot(x_data, y_data, settings):
    validate_array(x_data)
    validate_array(y_data)

    if len(x_data) != len(y_data):
        raise ValueError("x_data and y_data must have same length")

    x_data = to_array(x_data)
    y_data = to_array(y_data)

    create_figure()

    plt.scatter(
        x_data,
        y_data,
        color=settings["plot"]["color"],
        alpha=settings["plot"]["alpha"],
        marker=settings["plot"]["marker"],
        s=settings["plot"]["markersize"]
    )

    apply_plot_settings(
        title="Scatter Plot",
        x_label="X",
        y_label="Y",
        settings=settings
    )

    return build_plot_response(
        "scatter",
        {
            "x": x_data,
            "y": y_data
        }
    )

def plot_vectors(vector_list, settings):
    create_figure()

    vector_data = []

    for vector in vector_list:
        if len(vector) != 2:
            raise ValueError(
                "Each vector must contain exactly 2 coordinates (x, y)"
            )

        x = float(vector[0])
        y = float(vector[1])

        vector_data.append([x, y])

        plt.quiver(
            0, 0, x, y,
            color=settings["plot"]["color"]
        )

    plt.axhline(0)
    plt.axvline(0)
    plt.gca().set_aspect("equal")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Vector Plot")

    return build_plot_response(
        "vector",
        {
            "vectors": vector_data
        }
    )