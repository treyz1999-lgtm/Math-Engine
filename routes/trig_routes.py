from fastapi import APIRouter
from pydantic import BaseModel
import state
from services import trig
from utils.api_helpers import resolve_operation, safe_execute

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
