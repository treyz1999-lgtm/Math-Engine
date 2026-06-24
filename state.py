import copy


DEFAULT_SETTINGS = {
    "general": {
        "angle_mode": "degrees",
        "precision": 4
    },
    "plot": {
        "linewidth": 2,
        "color": "blue",
        "grid": True,
        "points": 500,
        "x_min": -10,
        "x_max": 10,
        "bins": 20,
        "alpha": 0.7,
        "marker": "o",
        "markersize": 5,
    },
    "calculus": {
        "epsilon": 0.1
    }
}

settings = copy.deepcopy(DEFAULT_SETTINGS)

history = []  # Stores past calculations as dictionaries returned by API calls.
              # Example:
              # {
              #     "operation": "derivative",
              #     "inputs": {"expr": "x^2", "variable": "x"},
              #     "output": "2*x"
              # }

def add_to_history(operation: str, inputs: dict, output):
    """
    Add a completed calculator operation to history.

    History is stored as a list of dictionaries where each entry
    represents one API call or calculator action.

    Each history entry contains:
        operation:
            The action performed by the user.

            Examples:
                "derivative"
                "vector_add"
                "plot_function"

        inputs:
            Dictionary containing all inputs required to perform
            the operation.

            A dictionary is used because many operations require
            multiple named inputs.

            Example:
                {
                    "v1": (1, 2),
                    "v2": (3, 4)
                }

        output:
            The result produced by the operation.

            Output type varies depending on the endpoint and may be:
                - numeric value
                - string expression
                - list / matrix
                - status message for visual operations

            Examples:
                2
                "2*x"
                [4, 6]
                "Displayed graph"

    Args:
        operation (str):
            Name of the operation performed.

        inputs (dict):
            Input parameters used for the operation.

        output:
            Output is intentionally untyped because it serves primarily as
            cached display data for history. The backend can always regenerate
            outputs from the stored operation and inputs.
    """
    history.append({
        "operation": operation,
        "inputs": inputs,
        "output": output,
    })

def clear_history():
    history.clear()

def get_history():
    return history

def get_history_entry(index: int):
    if index < 0 or index >= len(history):
        raise IndexError("Invalid history index")
    return history[index]

def delete_history_entry(index: int):
    if index < 0 or index >= len(history):
        raise IndexError("Invalid history index")

    removed = history.pop(index)
    return f"Removed history entry: {removed['operation']}"

def update_settings(category: str, setting: str, value):
    """
    Update a calculator setting with validation.

    Args:
        category (str):
            Settings category.
            Example: "general", "plot", "calculus"

        setting (str):
            Specific setting within the category.
            Example: "precision", "color", "epsilon"

        value:
            New value for the setting.

    Raises:
        ValueError:
            If category/setting is invalid or value fails validation.
    """
    if category not in settings:
        raise ValueError("Invalid settings category")

    if setting not in settings[category]:
        raise ValueError("Invalid setting")

    # GENERAL SETTINGS
    if category == "general" and setting == "angle_mode":
        if value not in ("degrees", "radians"):
            raise ValueError("angle_mode must be 'degrees' or 'radians'")

    if category == "general" and setting == "precision":
        value = int(value)
        if value < 0:
            raise ValueError("precision must be >= 0")

    # PLOT SETTINGS
    if category == "plot" and setting == "linewidth":
        value = float(value)
        if value <= 0:
            raise ValueError("linewidth must be > 0")

    if category == "plot" and setting == "color":
        if not isinstance(value, str):
            raise ValueError("color must be a string")

    if category == "plot" and setting == "grid":
        if not isinstance(value, bool):
            raise ValueError("grid must be boolean")

    if category == "plot" and setting == "points":
        value = int(value)
        if value < 2:
            raise ValueError("points must be at least 2")

    if category == "plot" and setting == "x_min":
        value = float(value)
        if value >= settings["plot"]["x_max"]:
            raise ValueError("x_min must be less than x_max")

    if category == "plot" and setting == "x_max":
        value = float(value)
        if value <= settings["plot"]["x_min"]:
            raise ValueError("x_max must be greater than x_min")

    if category == "plot" and setting == "bins":
        value = int(value)
        if value < 1:
            raise ValueError("bins must be at least 1")

    if category == "plot" and setting == "alpha":
        value = float(value)
        if not 0 <= value <= 1:
            raise ValueError("alpha must be between 0 and 1")

    if category == "plot" and setting == "marker":
        if not isinstance(value, str):
            raise ValueError("marker must be a string")

    if category == "plot" and setting == "markersize":
        value = float(value)
        if value <= 0:
            raise ValueError("markersize must be > 0")

    # CALCULUS SETTINGS
    if category == "calculus" and setting == "epsilon":
        value = float(value)
        if value <= 0:
            raise ValueError("epsilon must be > 0")

    settings[category][setting] = value

def reset_settings():
    settings.clear()
    settings.update(copy.deepcopy(DEFAULT_SETTINGS))
