import io
import base64
import matplotlib.pyplot as plt


def figure_to_base64() -> str:
    """
    Convert the current matplotlib figure into a base64 PNG string.

    This helper saves the active matplotlib figure into an in-memory
    buffer instead of writing to disk. The image is then encoded as a
    base64 string so it can be returned directly in JSON responses.

    Why use base64?
        Returning raw image bytes in JSON is inconvenient.

        Base64 allows the frontend to reconstruct the image using:

            data:image/png;base64,<encoded_string>

        This makes it easy to:
            - display fallback plot images
            - avoid temporary image files
            - avoid static file hosting during development

    After encoding, the figure is closed to prevent matplotlib memory
    leaks when many plots are generated.

    Returns:
        str:
            Base64-encoded PNG image of the current figure.
    """
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    return encoded

def apply_plot_settings(
    title: str,
    x_label: str,
    y_label: str,
    settings: dict
) -> None:
    """
    Apply common calculator plot settings to the current figure.

    This helper centralizes repeated matplotlib styling logic so each
    plot function remains focused on generating plot data rather than
    configuring chart appearance.

    Applied settings include:
        - title
        - x-axis label
        - y-axis label
        - grid visibility

    Styling values are read from the calculator settings state.

    Args:
        title (str):
            Plot title.

        x_label (str):
            Label for x-axis.

        y_label (str):
            Label for y-axis.

        settings (dict):
            Calculator settings dictionary.
    """
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(settings["plot"]["grid"])

import numpy as np


def serialize_plot_data(data):
    """
    Convert plot data into JSON-serializable Python types.

    Plot calculations often produce NumPy arrays or NumPy scalar types,
    which FastAPI cannot always serialize cleanly.

    This helper converts:
        - ndarray -> list
        - NumPy numeric types -> Python numeric types

    Args:
        data:
            Plot data object to serialize.

    Returns:
        JSON-serializable version of the data.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()

    if isinstance(data, np.generic):
        return data.item()

    return data

def build_plot_response(
    plot_type: str,
    plot_data: dict
) -> dict:
    """
    Build standardized API response for plot endpoints.

    Plot endpoints return two representations of the same graph:

        1. Structured plot data for frontend rendering
        2. Base64 PNG fallback image rendered by matplotlib

    Frontend priority:
        - Prefer interactive rendering using plot_data
        - Fallback to PNG if rendering fails

    This dual-response design provides resilience and flexibility.

    Args:
        plot_type (str):
            Type of plot.

            Examples:
                "line"
                "scatter"
                "histogram"
                "boxplot"

        plot_data (dict):
            Plot coordinate and metadata payload.

    Returns:
        dict:
            Standardized plot response.
    """
    cleaned_data = {
        key: serialize_plot_data(value)
        for key, value in plot_data.items()
    }

    return {
        "plot_type": plot_type,
        "plot_data": cleaned_data,
        "png": figure_to_base64()
    }

def create_figure():
    """
    Create a fresh matplotlib figure.

    Using a fresh figure for every request prevents plot overlap
    between API calls when multiple requests hit the backend.

    This is especially important for persistent FastAPI processes.

    Returns:
        None
    """
    plt.figure()