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

history = []



# HISTORY

def add_to_history(endpoint: str, request_data: dict, output, display_name: str):
    history.append({
        "endpoint": endpoint,
        "request": request_data,
        "display_name": display_name,
        "output": output
    })


def clear_history():
    history.clear()


def get_history():
    return history.copy()


def get_history_entry(index: int):
    if index < 0 or index >= len(history):
        raise IndexError("Invalid history index")
    return history[index]


def delete_history_entry(index: int):
    if index < 0 or index >= len(history):
        raise IndexError("Invalid history index")

    removed = history.pop(index)
    return f"Removed history entry: {removed['display_name']}"



# SETTING VALIDATORS

def validate_angle_mode(value):
    if value not in ("degrees", "radians"):
        raise ValueError("angle_mode must be 'degrees' or 'radians'")
    return value


def validate_precision(value):
    value = int(value)
    if value < 0:
        raise ValueError("precision must be >= 0")
    return value


def validate_linewidth(value):
    value = float(value)
    if value <= 0:
        raise ValueError("linewidth must be > 0")
    return value


def validate_color(value):
    if not isinstance(value, str):
        raise ValueError("color must be a string")
    return value


def validate_grid(value):
    if not isinstance(value, bool):
        raise ValueError("grid must be boolean")
    return value


def validate_points(value):
    value = int(value)
    if value < 2:
        raise ValueError("points must be at least 2")
    return value


def validate_x_min(value):
    value = float(value)
    if value >= settings["plot"]["x_max"]:
        raise ValueError("x_min must be less than x_max")
    return value


def validate_x_max(value):
    value = float(value)
    if value <= settings["plot"]["x_min"]:
        raise ValueError("x_max must be greater than x_min")
    return value


def validate_bins(value):
    value = int(value)
    if value < 1:
        raise ValueError("bins must be at least 1")
    return value


def validate_alpha(value):
    value = float(value)
    if not 0 <= value <= 1:
        raise ValueError("alpha must be between 0 and 1")
    return value


def validate_marker(value):
    if not isinstance(value, str):
        raise ValueError("marker must be a string")
    return value


def validate_markersize(value):
    value = float(value)
    if value <= 0:
        raise ValueError("markersize must be > 0")
    return value


def validate_epsilon(value):
    value = float(value)
    if value <= 0:
        raise ValueError("epsilon must be > 0")
    return value


SETTING_VALIDATORS = {
    "general": {
        "angle_mode": validate_angle_mode,
        "precision": validate_precision,
    },
    "plot": {
        "linewidth": validate_linewidth,
        "color": validate_color,
        "grid": validate_grid,
        "points": validate_points,
        "x_min": validate_x_min,
        "x_max": validate_x_max,
        "bins": validate_bins,
        "alpha": validate_alpha,
        "marker": validate_marker,
        "markersize": validate_markersize,
    },
    "calculus": {
        "epsilon": validate_epsilon
    }
}



# SETTINGS

def update_settings(category: str, setting: str, value):
    """
    Update calculator settings using validator map.
    """
    validator = SETTING_VALIDATORS.get(category, {}).get(setting) #validator becomes equal to the function from the map

    if validator is None:
        raise ValueError("Invalid settings category or setting")

    cleaned_value = validator(value)
    settings[category][setting] = cleaned_value


def reset_settings():
    settings.clear()
    settings.update(copy.deepcopy(DEFAULT_SETTINGS))