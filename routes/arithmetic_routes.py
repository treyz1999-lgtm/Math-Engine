from fastapi import APIRouter
from pydantic import BaseModel
from services import arithmetic
from utils.api_helpers import execute_and_log

router = APIRouter(
    prefix="/arithmetic",
    tags=["Arithmetic"],
)

# FUNCTION MAPS
BINARY_FUNCTIONS = {
    "add": arithmetic.add,
    "subtract": arithmetic.subtract,
    "multiply": arithmetic.multiply,
    "divide": arithmetic.divide,
    "mod": arithmetic.mod,
    "root": arithmetic.root,
}

POWER_FUNCTIONS = {
    "power": arithmetic.power,
}

OTHER_FUNCTIONS = {
    "abs": arithmetic.absolute_value,
    "factorial": arithmetic.factorial,
}

# REQUEST MODELS
class BasicArithmeticRequest(BaseModel):
    operation: str
    value1: float
    value2: float


class PowerArithmeticRequest(BaseModel):
    operation: str
    base: float
    exponent: int


class OtherArithmeticRequest(BaseModel):
    operation: str
    value1: float

# ROUTES
@router.post("/binary")
def base_arithmetic_endpoint(request: BasicArithmeticRequest) -> dict:
    _, result = execute_and_log(
        "/arithmetic/binary",
        request,
        BINARY_FUNCTIONS,
        "binary",
        request.value1,
        request.value2
    )
    return {"result": result}

@router.post("/power")
def power_arithmetic_endpoint(request: PowerArithmeticRequest) -> dict:
    _, result = execute_and_log(
        "/arithmetic/power",
        request,
        POWER_FUNCTIONS,
        "power",
        request.base,
        request.exponent
    )
    return {"result": result}

@router.post("/other")
def other_arithmetic_endpoint(request: OtherArithmeticRequest) -> dict:
    _, result = execute_and_log(
        "/arithmetic/other",
        request,
        OTHER_FUNCTIONS,
        "other",
        request.value1,
    )
    return {"result": result}

