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
} #ideally we will not touch this, and we can just modify a copy for any user changes, this makes resting settings trivial

settings = copy.deepcopy(DEFAULT_SETTINGS)
history = []

# HISTORY
def add_to_history(endpoint: str, request_data: dict, output, display_name: str):
    """
       Store a completed calculator API request in history.

       Each history entry contains enough information to both display
       the calculation in a frontend history panel and replay the exact
       request later without requiring the user to manually re-enter inputs.

       Stored fields:
           endpoint:
               API route used to perform the calculation.

               Example:
                   "/trig/basic"
                   "/expressions/calculus/derivative"

               This allows the frontend (or backend) to know which
               endpoint should be called again when replaying.

           request:
               Original JSON request payload sent to the endpoint.

               Example:
                   {
                       "operation": "sin",
                       "value": 45
                   }

               This makes replay simple because the exact request body
               can be sent again without rebuilding inputs manually.

           display_name:
               Human-readable label used for frontend history display.

               Example:
                   "Trig: sin"
                   "Derivative"
                   "Law of Cosines: solve_side"

           output:
               Cached result returned by the original calculation.

               This allows the frontend to immediately show prior results
               without recomputing unless replay is requested.

       Why store endpoint + request separately?
           Together, these fields make history replay straightforward.

           A previous calculation can be rerun by retrieving a history entry:

               history[index]["endpoint"]
               history[index]["request"]

           Then simply sending:

               POST endpoint with request payload

           This design decouples replay logic from calculator menus,
           allowing users to rerun past calculations directly from history.
       """
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
    settings.update(copy.deepcopy(DEFAULT_SETTINGS)) #copy keys and values