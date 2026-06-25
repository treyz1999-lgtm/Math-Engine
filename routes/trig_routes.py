from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import state
from services import trig

router = APIRouter(
    prefix="/trig",
    tags=["Trigonometry"]
)

# HELPERS

def resolve_operation(operation: str, function_map: dict, family: str):
    """
    Normalize an operation string and resolve its mapped function.

    This helper is used by API endpoints that support multiple operations
    through a single route. It converts the user-provided operation to
    lowercase, looks up the corresponding function in a dispatch map,
    and returns both the normalized operation and function reference.

    Example:
        function_map = {
            "sin": trig.trig_sin,
            "cos": trig.trig_cos
        }

        Input:
            operation = "SIN"

        Output:
            ("sin", trig.trig_sin)

    Args:
        operation (str):
            Operation name provided by the request payload.

            Example:
                "sin"
                "solve_side"
                "matrix_inverse"

        function_map (dict):
            Dictionary mapping operation names to function references.

            Example:
                {
                    "sin": trig.trig_sin,
                    "cos": trig.trig_cos
                }

        family (str):
            Name of the operation group used for error messaging.

            Example:
                "trig"
                "linear algebra"
                "calculus"

    Returns:
        tuple[str, callable]:
            A tuple containing:
                - normalized operation string
                - resolved function reference

    Raises:
        HTTPException:
            Status code 400 if the operation is invalid or not found
            in the provided function map.
    """
    operation = operation.lower()
    func = function_map.get(operation)

    if func is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {family} operation"
        )

    return operation, func

def safe_execute(func, *args):
    """
      Execute a function safely and convert ValueErrors into HTTP errors.

      This helper wraps service-layer function calls so API routes do not
      need repetitive try/except blocks. Any ValueError raised by the
      underlying function is converted into an HTTP 400 response.

      The *args parameter allows this helper to accept an arbitrary number
      of positional arguments.

      Example:
          safe_execute(func, arg1)
          safe_execute(func, arg1, arg2)
          safe_execute(func, arg1, arg2, arg3, settings)

      How *args works:
          *args collects all extra positional arguments into a tuple.

          Example:
              safe_execute(func, 1, 2, 3)

          Inside the function:
              args == (1, 2, 3)

          When calling:
              func(*args)

          Python unpacks the tuple back into separate arguments:

              func(1, 2, 3)

      This is useful because calculator functions have different signatures.

      Examples:
          trig_sin(angle, settings)
          triangle_leg(hypotenuse, leg)
          law_of_sines(side, angle, target, settings)

      Using *args allows one helper to support all of them.

      Args:
          func:
              Function reference to execute.

          *args:
              Arbitrary positional arguments passed to func.

      Returns:
          The result returned by func.

      Raises:
          HTTPException:
              Status code 400 if func raises a ValueError.
      """
    try:
        return func(*args)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#FUNCTION MAPS

BASIC_TRIG_FUNCTIONS = {
    "sin": trig.trig_sin,
    "cos": trig.trig_cos,
    "tan": trig.trig_tan,
    "sec": trig.trig_sec,
    "csc": trig.trig_csc,
    "cot": trig.trig_cot,
    "arcsin": trig.trig_arcsin,
    "arccos": trig.trig_arccos,
    "arctan": trig.trig_arctan,
}

LAW_OF_SINES_FUNCTIONS = {
    "solve_side": trig.triangle_side_law_of_sines,
    "solve_angle": trig.triangle_angle_law_of_sines,
}

LAW_OF_COSINES_FUNCTIONS = {
    "solve_side": trig.triangle_side_law_of_cosines,
    "solve_angle": trig.triangle_angle_law_of_cosines,
}

TRIANGLE_HELPER_FUNCTIONS = {
    "hypotenuse": trig.triangle_hypotenuse,
    "leg": trig.triangle_leg,
    "third_angle": trig.triangle_third_angle,
}

UNIT_CIRCLE_FUNCTIONS = {
    'coordinates' : trig.unit_circle_coordinates,
    'quadrant' : trig.unit_circle_quadrant,
}

# REQUEST MODELS

class BasicTrigRequest(BaseModel):
    operation: str
    value: float  # angle for basic trig, ratio/value for inverse trig


class LawOfSinesTrigRequest(BaseModel):
    operation: str
    known_side: float
    known_angle: float
    target_value: float


class LawOfCosinesTrigRequest(BaseModel):
    operation: str
    side1: float
    side2: float
    value3: float  # either angle or side


class TriangleHelperRequest(BaseModel):
    operation: str
    value1: float
    value2: float

class UnitCircleRequest(BaseModel):
    operation: str
    angle: float

# ROUTES

@router.post("/basic")
def basic_trig_endpoint(request: BasicTrigRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        BASIC_TRIG_FUNCTIONS,
        "trig"
    )

    result = safe_execute(
        func,
        request.value,
        state.settings
    )

    state.add_to_history(
        endpoint="/trig/basic",
        request_data=request.model_dump(),
        display_name=f"Trig: {operation}",
        output=result
    )

    return {"result": result}

@router.post("/law-of-sines")
def law_of_sines_endpoint(request: LawOfSinesTrigRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        LAW_OF_SINES_FUNCTIONS,
        "law-of-sines"
    )

    result = safe_execute(
        func,
        request.known_side,
        request.known_angle,
        request.target_value,
        state.settings
    )

    state.add_to_history(
        endpoint="/trig/law-of-sines",
        request_data=request.model_dump(),
        display_name=f"Law of Sines: {operation}",
        output=result
    )

    return {"result": result}

@router.post("/law-of-cosines")
def law_of_cosines_endpoint(request: LawOfCosinesTrigRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        LAW_OF_COSINES_FUNCTIONS,
        "law-of-cosines"
    )

    result = safe_execute(
        func,
        request.side1,
        request.side2,
        request.value3,
        state.settings
    )

    state.add_to_history(
        endpoint="/trig/law-of-cosines",
        request_data=request.model_dump(),
        display_name=f"Law of Cosines: {operation}",
        output=result
    )

    return {"result": result}

@router.post("/triangle-helpers")
def triangle_helper_endpoint(request: TriangleHelperRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        TRIANGLE_HELPER_FUNCTIONS,
        "triangle-helper"
    )

    if operation == "third_angle":
        result = safe_execute(
            func,
            request.value1,
            request.value2,
            state.settings
        )
    else:
        result = safe_execute(
            func,
            request.value1,
            request.value2
        )

    state.add_to_history(
        endpoint="/trig/triangle-helpers",
        request_data=request.model_dump(),
        display_name=f"Triangle Helper: {operation}",
        output=result
    )

    return {"result": result}

@router.post('/unit-circle')
def unit_circle_endpoint(request: UnitCircleRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        UNIT_CIRCLE_FUNCTIONS,
        'unit-circle'
    )
    result = safe_execute(
        func,
        request.angle,
        state.settings
    )
    state.add_to_history(
        endpoint="/trig/unit-circle",
        request_data=request.model_dump(),
        display_name=f"Find Unit-Circle: {operation}",
        output=result
    )
    return {"result": result}
