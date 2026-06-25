from fastapi import APIRouter
from pydantic import BaseModel
from services import geometry_3d
from utils.api_helpers import execute_and_log

router = APIRouter(
    prefix="/geometry-3d",
    tags=["Geometry 3D"]
)

#Function Mapping
SINGLE_INPUT_FUNCTIONS = {
    "cube_volume": geometry_3d.cube_volume,
    "cube_surface_area": geometry_3d.cube_surface_area,
    "cube_edge_sum": geometry_3d.cube_edge_sum,
    "sphere_volume": geometry_3d.sphere_volume,
    "sphere_surface_area": geometry_3d.sphere_surface_area,
}

TWO_INPUT_FUNCTIONS = {
    "cylinder_volume": geometry_3d.cylinder_volume,
    "cylinder_surface_area": geometry_3d.cylinder_surface_area,
    "cone_slant_height": geometry_3d.cone_slant_height,
    "cone_volume": geometry_3d.cone_volume,
    "cone_surface_area": geometry_3d.cone_surface_area,
    "pyramid_volume": geometry_3d.pyramid_volume,
}

THREE_INPUT_FUNCTIONS = {
    "prism_volume": geometry_3d.prism_volume,
    "prism_surface_area": geometry_3d.prism_surface_area,
    "prism_diagonal": geometry_3d.prism_diagonal,
}

#Request models
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

#routes
@router.post("/single-input")
def single_input_endpoint(request: SingleInputRequest):
    _, result = execute_and_log(
        "/geometry-3d/single-input",
        request,
        SINGLE_INPUT_FUNCTIONS,
        "Geometry 3D",
        request.value
    )
    return {"result": result}

@router.post("/two-input")
def two_input_endpoint(request: TwoInputRequest):
    _, result = execute_and_log(
        "/geometry-3d/two-input",
        request,
        TWO_INPUT_FUNCTIONS,
        "Geometry 3D",
        request.value1,
        request.value2
    )
    return {"result": result}

@router.post("/three-input")
def three_input_endpoint(request: ThreeInputRequest):
    _, result = execute_and_log(
        "/geometry-3d/three-input",
        request,
        THREE_INPUT_FUNCTIONS,
        "Geometry 3D",
        request.value1,
        request.value2,
        request.value3
    )
    return {"result": result}