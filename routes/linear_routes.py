from fastapi import APIRouter
from pydantic import BaseModel
from services import linear
from utils.api_helpers import execute_and_log

router = APIRouter(
    prefix="/linear",
    tags=["Linear Algebra"]
)

#function maps
VECTOR_PAIR_FUNCTIONS = {
    "vector_add": linear.vector_add,
    "vector_subtract": linear.vector_subtract,
    "vector_dot_product": linear.vector_dot_product,
    "vector_cross_product": linear.vector_cross_product,
}

VECTOR_SINGLE_FUNCTIONS = {
    "vector_magnitude": linear.vector_magnitude,
    "vector_unit": linear.vector_unit,
}

VECTOR_SCALAR_FUNCTIONS = {
    "vector_scalar_multiply": linear.vector_scalar_multiply,
}

MATRIX_PAIR_FUNCTIONS = {
    "matrix_add": linear.matrix_add,
    "matrix_subtract": linear.matrix_subtract,
    "matrix_multiply": linear.matrix_multiply,
}

MATRIX_SINGLE_FUNCTIONS = {
    "matrix_transpose": linear.matrix_transpose,
    "matrix_determinant": linear.matrix_determinant,
    "matrix_inverse": linear.matrix_inverse,
    "matrix_trace": linear.matrix_trace,
    "matrix_rank": linear.matrix_rank,
    "matrix_eigenvalues": linear.matrix_eigenvalues,
    "matrix_eigenvectors": linear.matrix_eigenvectors,
    "matrix_svd": linear.matrix_svd,
}

MATRIX_SCALAR_FUNCTIONS = {
    "matrix_scalar_multiply": linear.matrix_scalar_multiply,
}

LINEAR_SYSTEM_FUNCTIONS = {
    "solve_linear_system": linear.solve_linear_system,
}

#request models
class VectorPairRequest(BaseModel):
    operation: str
    vector_1: list[float]
    vector_2: list[float]


class VectorSingleRequest(BaseModel):
    operation: str
    vector: list[float]


class VectorScalarRequest(BaseModel):
    operation: str
    vector: list[float]
    scalar: float


class MatrixPairRequest(BaseModel):
    operation: str
    matrix_1: list[list[float]]
    matrix_2: list[list[float]]


class MatrixSingleRequest(BaseModel):
    operation: str
    matrix: list[list[float]]


class MatrixScalarRequest(BaseModel):
    operation: str
    matrix: list[list[float]]
    scalar: float


class LinearSystemRequest(BaseModel):
    operation: str
    coefficient_matrix: list[list[float]]
    constant_vector: list[float]

#routes
@router.post("/vector-pair")
def vector_pair_endpoint(request: VectorPairRequest):
    _, result = execute_and_log(
        "/linear/vector-pair",
        request,
        VECTOR_PAIR_FUNCTIONS,
        "Linear Algebra",
        request.vector_1,
        request.vector_2
    )
    return {"result": result}

@router.post("/vector-single")
def vector_single_endpoint(request: VectorSingleRequest):
    _, result = execute_and_log(
        "/linear/vector-single",
        request,
        VECTOR_SINGLE_FUNCTIONS,
        "Linear Algebra",
        request.vector
    )
    return {"result": result}

@router.post("/vector-scalar")
def vector_scalar_endpoint(request: VectorScalarRequest):
    _, result = execute_and_log(
        "/linear/vector-scalar",
        request,
        VECTOR_SCALAR_FUNCTIONS,
        "Linear Algebra",
        request.vector,
        request.scalar
    )
    return {"result": result}

@router.post("/matrix-pair")
def matrix_pair_endpoint(request: MatrixPairRequest):
    _, result = execute_and_log(
        "/linear/matrix-pair",
        request,
        MATRIX_PAIR_FUNCTIONS,
        "Linear Algebra",
        request.matrix_1,
        request.matrix_2
    )
    return {"result": result}

@router.post("/matrix-single")
def matrix_single_endpoint(request: MatrixSingleRequest):
    _, result = execute_and_log(
        "/linear/matrix-single",
        request,
        MATRIX_SINGLE_FUNCTIONS,
        "Linear Algebra",
        request.matrix
    )
    return {"result": result}

@router.post("/matrix-scalar")
def matrix_scalar_endpoint(request: MatrixScalarRequest):
    _, result = execute_and_log(
        "/linear/matrix-scalar",
        request,
        MATRIX_SCALAR_FUNCTIONS,
        "Linear Algebra",
        request.matrix,
        request.scalar
    )
    return {"result": result}

@router.post("/solve-system")
def solve_system_endpoint(request: LinearSystemRequest):
    _, result = execute_and_log(
        "/linear/solve-system",
        request,
        LINEAR_SYSTEM_FUNCTIONS,
        "Linear Algebra",
        request.coefficient_matrix,
        request.constant_vector
    )
    return {"result": result}