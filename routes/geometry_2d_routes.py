from fastapi import APIRouter
from pydantic import BaseModel
from services import geometry_2d
from utils.api_helpers import execute_and_log, resolve_operation, safe_execute
import state

router = APIRouter(
    prefix="/geometry-2d",
    tags=["Geometry 2D"]
)

#Function Mapping - done based on input count as most functions here are accepting the same/ similar data types
SINGLE_INPUT_FUNCTIONS = {
    "square_area": geometry_2d.square_area,
    "square_perimeter": geometry_2d.square_perimeter,
    "square_diagonal": geometry_2d.square_diagonal,
    "circle_area": geometry_2d.circle_area,
    "circle_circumference": geometry_2d.circle_circumference,
}

TWO_INPUT_FUNCTIONS = {
    "rectangle_area": geometry_2d.rectangle_area,
    "rectangle_perimeter": geometry_2d.rectangle_perimeter,
    "rectangle_diagonal": geometry_2d.rectangle_diagonal,
    "triangle_area_right": geometry_2d.triangle_area_right,
    "triangle_area_isosceles": geometry_2d.triangle_area_isosceles,
    "parallelogram_area": geometry_2d.parallelogram_area,
    "parallelogram_perimeter": geometry_2d.parallelogram_perimeter,
}

THREE_INPUT_FUNCTIONS = {
    "triangle_area_sss": geometry_2d.triangle_area_sss,
    "triangle_perimeter": geometry_2d.triangle_perimeter,
    "trapezoid_area": geometry_2d.trapezoid_area,
}
#remaining functions will not use/ need mapping

#request models
class SingleInputRequest(BaseModel):
    operation: str
    value: float


class TwoInputRequest(BaseModel):
    operation: str
    value1: float
    value2: float


class ThreeInputRequest(BaseModel):
    operation: str
    value1: float
    value2: float
    value3: float


class TrapezoidPerimeterRequest(BaseModel):
    side1: float
    side2: float
    side3: float
    side4: float


class PolygonRequest(BaseModel):
    operation: str
    sides: int
    side_length: float | None = None

#routes
@router.post("/single-input")
def single_input_endpoint(request: SingleInputRequest):
    _, result = execute_and_log(
        "/geometry-2d/single-input",
        request,
        SINGLE_INPUT_FUNCTIONS,
        "Geometry 2D",
        request.value
    )
    return {"result": result}

@router.post("/two-input")
def two_input_endpoint(request: TwoInputRequest):
    _, result = execute_and_log(
        "/geometry-2d/two-input",
        request,
        TWO_INPUT_FUNCTIONS,
        "Geometry 2D",
        request.value1,
        request.value2
    )
    return {"result": result}

@router.post("/three-input")
def three_input_endpoint(request: ThreeInputRequest):
    _, result = execute_and_log(
        "/geometry-2d/three-input",
        request,
        THREE_INPUT_FUNCTIONS,
        "Geometry 2D",
        request.value1,
        request.value2,
        request.value3
    )
    return {"result": result}

@router.post("/trapezoid-perimeter")
def trapezoid_perimeter_endpoint(request: TrapezoidPerimeterRequest):
    result = safe_execute(
        geometry_2d.trapezoid_perimeter,
        request.side1,
        request.side2,
        request.side3,
        request.side4
    )

    state.add_to_history(
        endpoint="/geometry-2d/trapezoid-perimeter",
        request_data=request.model_dump(),
        display_name="Geometry 2D: trapezoid_perimeter",
        output=result
    )

    return {"result": result}

#polygons are too varied to easily map, so they are manually handled here
@router.post("/polygon")
def polygon_endpoint(request: PolygonRequest):
    operation = request.operation.lower()

    if operation == "regular_polygon_area":
        result = safe_execute(
            geometry_2d.regular_polygon_area,
            request.sides,
            request.side_length
        )

    elif operation == "regular_polygon_perimeter":
        result = safe_execute(
            geometry_2d.regular_polygon_perimeter,
            request.sides,
            request.side_length
        )

    elif operation == "polygon_interior_angle_sum":
        result = safe_execute(
            geometry_2d.polygon_interior_angle_sum,
            request.sides
        )

    elif operation == "regular_polygon_interior_angle":
        result = safe_execute(
            geometry_2d.regular_polygon_interior_angle,
            request.sides
        )

    else:
        raise ValueError("Invalid operation")

    state.add_to_history(
        endpoint="/geometry-2d/polygon",
        request_data=request.model_dump(),
        display_name=f"Geometry 2D: {operation}",
        output=result
    )

    return {"result": result}