from fastapi import APIRouter
from pydantic import BaseModel
import state
from services import trig
from utils.api_helpers import resolve_operation, safe_execute, execute_and_log

router = APIRouter(
    prefix="/trig",
    tags=["Trigonometry"]
)

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
def basic_trig_endpoint(request: BasicTrigRequest):
    _, result = execute_and_log(
        "/trig/basic",
        request,
        BASIC_TRIG_FUNCTIONS,
        "Trig",
        request.value,
        state.settings
    )
    return {"result": result}

@router.post("/law-of-sines")
def law_of_sines_endpoint(request: LawOfSinesTrigRequest):
    _, result = execute_and_log(
        "/trig/law-of-sines",
        request,
        LAW_OF_SINES_FUNCTIONS,
        "Law of Sines",
        request.known_side,
        request.known_angle,
        request.target_value,
        state.settings
    )
    return {"result": result}

@router.post("/law-of-cosines")
def law_of_cosines_endpoint(request: LawOfCosinesTrigRequest):
    _, result = execute_and_log(
        "/trig/law-of-cosines",
        request,
        LAW_OF_COSINES_FUNCTIONS,
        "Law of Cosines",
        request.side1,
        request.side2,
        request.value3,
        state.settings
    )
    return {"result": result}

@router.post("/triangle-helpers")
def triangle_helper_endpoint(request: TriangleHelperRequest):
    operation, func = resolve_operation(
        request.operation,
        TRIANGLE_HELPER_FUNCTIONS
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

@router.post("/unit-circle")
def unit_circle_endpoint(request: UnitCircleRequest):
    _, result = execute_and_log(
        "/trig/unit-circle",
        request,
        UNIT_CIRCLE_FUNCTIONS,
        "Unit Circle",
        request.angle,
        state.settings
    )
    return {"result": result}
