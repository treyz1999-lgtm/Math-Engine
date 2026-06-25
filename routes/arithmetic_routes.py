from fastapi import APIRouter
from pydantic import BaseModel

import state
from services import arithmetic
from utils.api_helpers import resolve_operation, safe_execute

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
    operation, func = resolve_operation(
        request.operation,
        BINARY_FUNCTIONS,
        "binary"
    )

    result = safe_execute(
        func,
        request.value1,
        request.value2
    )

    state.add_to_history(
        endpoint="/arithmetic/base",
        request_data=request.model_dump(),
        display_name=f"Result of {operation}",
        output=result
    )

    return {"result": result}

@router.post("/power")
def power_arithmetic_endpoint(request: PowerArithmeticRequest) -> dict:
    operation, func = resolve_operation(
        request.operation,
        POWER_FUNCTIONS,
        "power"
    )

    result = safe_execute(
        func,
        request.base,
        request.exponent
    )

    state.add_to_history(
        endpoint="/arithmetic/power",
        request_data=request.model_dump(),
        display_name=f"Result of {operation}",
        output=result
    )

    return {"result": result}