from fastapi import APIRouter
from pydantic import BaseModel
from services import stats
from utils.api_helpers import execute_and_log

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)

# FUNCTION MAPS
SINGLE_ARRAY_FUNCTIONS = {
    "mean": stats.stats_mean,
    "median": stats.stats_median,
    "mode": stats.stats_mode,
    "range": stats.stats_range,
    "quartiles": stats.stats_quartiles,
    "iqr": stats.stats_iqr,
}

ARRAY_SCALAR_FUNCTIONS = {
    "variance": stats.stats_variance,
    "std": stats.stats_std,
    "percentile": stats.stats_percentile,
}

TWO_ARRAY_FUNCTIONS = {
    "covariance": stats.stats_covariance,
    "correlation": stats.stats_correlation,
}

COMBINATORICS_FUNCTIONS = {
    "permutations": stats.stats_permutations,
    "combinations": stats.stats_combinations,
}

Z_SCORE_FUNCTIONS = {
    "z_score": stats.stats_z_score,
}

# REQUEST MODELS
class SingleArrayRequest(BaseModel):
    operation: str
    data: list[float]

class ArrayScalarRequest(BaseModel):
    operation: str
    data: list[float]
    value: float
    # value = percentile OR degrees_of_freedom depending on operation

class TwoArrayRequest(BaseModel):
    operation: str
    dataset_1: list[float]
    dataset_2: list[float]

class CombinatoricsRequest(BaseModel):
    operation: str
    total_items: int
    selected_items: int

class ZScoreRequest(BaseModel):
    operation: str
    value: float
    mean: float
    standard_deviation: float

# ROUTES
@router.post("/single-array")
def single_array_endpoint(request: SingleArrayRequest):
    _, result = execute_and_log(
        "/stats/single-array",
        request,
        SINGLE_ARRAY_FUNCTIONS,
        "Stats",
        request.data
    )
    return {"result": result}

@router.post("/array-scalar")
def array_scalar_endpoint(request: ArrayScalarRequest):
    _, result = execute_and_log(
        "/stats/array-scalar",
        request,
        ARRAY_SCALAR_FUNCTIONS,
        "Stats",
        request.data,
        request.value
    )
    return {"result": result}

@router.post("/two-arrays")
def two_arrays_endpoint(request: TwoArrayRequest):
    _, result = execute_and_log(
        "/stats/two-arrays",
        request,
        TWO_ARRAY_FUNCTIONS,
        "Stats",
        request.dataset_1,
        request.dataset_2
    )
    return {"result": result}

@router.post("/combinatorics")
def combinatorics_endpoint(request: CombinatoricsRequest):
    _, result = execute_and_log(
        "/stats/combinatorics",
        request,
        COMBINATORICS_FUNCTIONS,
        "Stats",
        request.total_items,
        request.selected_items
    )
    return {"result": result}

@router.post("/z-score")
def z_score_endpoint(request: ZScoreRequest):
    _, result = execute_and_log(
        "/stats/z-score",
        request,
        Z_SCORE_FUNCTIONS,
        "Stats",
        request.value,
        request.mean,
        request.standard_deviation
    )
    return {"result": result}