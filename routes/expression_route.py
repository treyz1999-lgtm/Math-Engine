from fastapi import APIRouter
from pydantic import BaseModel
import state
from typing import Any
from services import expression_engine as ex
from utils.api_helpers import resolve_operation, safe_execute, serialize_result

router = APIRouter(
    prefix="/expressions",
    tags=["Expression"],
)

# FUNCTION MAPS

MANIPULATE_EXPRESSION = {
    'simplify' : ex.simplify_expression,
    'expand' : ex.expand_expression,
    'factor' : ex.factor_expression,
}

EVALUATE_EXPRESSION = {
    'evaluate' : ex.evaluate_expression,
}

"""
solving:
    /expressions/solve
    solve_equation
    solve_system
    solve_quadratic
    find_roots
"""
SOLVE_EQUATION = {
    'linear_equation' : ex.solve_linear_equation,
    'equation' : ex.solve_equation,
}

SOLVE_QUADRATIC = {
    'quadratic_equation' : ex.solve_quadratic,
}

SOLVE_SYSTEM = {
    'system' : ex.solve_system,
}

SOLVE_ROOTS = {
    'roots' : ex.find_roots,
}



"""
calculus:
    /expressions/calculus
    derivative
    integral
    limit
"""

"""
Function analysis:
    /expressions/analyze
    domain
    intercepts
    critical points
    extrema
    inflection points
"""


# REQUEST MODELS

class ManipulateExpressionRequest(BaseModel):
    operation: str
    expr : str

class EvaluateExpressionRequest(BaseModel):
    operation: str
    expr : str
    variables: dict[str, float] | None = None

class SolveEquationRequest(BaseModel):
    operation: str
    left_hand : str
    right_hand : str
    variable : str

class SolveQuadraticRequest(BaseModel):
    operation: str
    value1 : float
    value2 : float
    value3 : float

# ROUTES

@router.post("/manipulate")
def manipulate_expression_endpoint(request: ManipulateExpressionRequest):
    operation, func = resolve_operation(
        request.operation,
        MANIPULATE_EXPRESSION,
        'expression',
    )

    result = safe_execute(
        func,
        request.expr
    )
    result = serialize_result(result)

    state.add_to_history(
        endpoint="/expression/manipulate",
        request_data=request.model_dump(),
        display_name=f"{operation} expression",
        output=result
    )
    return {'result': result}

@router.post("/evaluate")
def evaluate_expression_endpoint(request: EvaluateExpressionRequest):
    operation, func = resolve_operation(
        request.operation,
        EVALUATE_EXPRESSION,
        'expression',
    )

    result = safe_execute(
        func,
        request.expr,
        request.variables,
    )
    result = serialize_result(result)

    state.add_to_history(
        endpoint="/expression/evaluate",
        request_data=request.model_dump(),
        display_name=f"{operation} expression",
        output=result
    )

    return {'result': result}

@router.post("/solve/equation")
def solve_equation_endpoint(request: SolveEquationRequest):
    operation, func = resolve_operation(
        request.operation,
        SOLVE_EQUATION,
        'expression',
    )

    result = safe_execute(
        func,
        request.left_hand,
        request.right_hand,
        request.variable
    )

    result = serialize_result(result)

    state.add_to_history(
        endpoint="/expression/solve/equation",
        request_data=request.model_dump(),
        display_name=f" solve {operation} ",
        output=result
    )

    return {'result': result}

@router.post("/solve/quadratic")
def solve_quadratic_endpoint(request: SolveQuadraticRequest):
    operation, func = resolve_operation(
        request.operation,
        SOLVE_QUADRATIC,
        'expression',
    )

    result = safe_execute(
        func,
        request.value1,
        request.value2,
        request.value3,
    )

    result = serialize_result(result)

    state.add_to_history(
        endpoint="/expression/solve/quadratic",
        request_data=request.model_dump(),
        display_name=f" solve {operation} ",
        output=result
    )

    return {'result': result}