from fastapi import APIRouter
from pydantic import BaseModel
import state
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

FIND_DERIVATIVE = {
    'derivative' : ex.derivative,
}

FIND_INTEGRAL = {
    'integral' : ex.integral,
}

FIND_LIMIT = {
    'limit' : ex.limit,
}
"""
Function analysis:
    /expressions/analyze
    domain
    intercepts
    critical points -1
    extrema - 1
    inflection points
"""
FIND_DOMAIN = {
    'domain' : ex.function_domain
}

FIND_INTERCEPTS = {
    'intercepts' : ex.function_intercepts
}

FIND_CRIT_POINTS = {
    'critical points' : ex.critical_points,
    'local_extrema' : ex.local_extrema,
}

FIND_INFLECTIONS = {
    'inflection points' : ex.inflection_points,
}


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

class SolveSystemRequest(BaseModel):
    operation: str
    equations : list[str]
    variables : list[str]

class FindRootsRequest(BaseModel):
    operation: str
    expr : str
    variable : str

class FindDerivativeRequest(BaseModel):
    operation: str
    expr : str
    variable : str
    order: int

class FindIntegralRequest(BaseModel):
    operation: str
    expr : str
    variable : str
    lower_bound : int | float | str | None = None
    upper_bound: int | float | str | None = None

class FindLimitRequest(BaseModel):
    operation: str
    expr : str
    variable : str
    value : int | float | str

class FindDomainRequest(BaseModel):
    operation: str
    expr : str
    variable : str
    math_set : str | None = None

class FindInterceptsRequest(BaseModel):
    operation: str
    expr : str

class FindCriticalPointsRequest(BaseModel):
    operation: str
    expr : str
    variable : str

class FindInflectionPointsRequest(BaseModel):
    operation: str
    expr : str
    variable : str
    epsilon : float

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

@router.post("/solve/system")
def solve_system_endpoint(request: SolveSystemRequest):
    operation, func = resolve_operation(
        request.operation,
        SOLVE_SYSTEM,
        'expression',
    )
    result = safe_execute(
        func,
        request.equations,
        request.variables,
    )

    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/solve/system",
        request_data=request.model_dump(),
        display_name=f" solve {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/solve/roots")
def solve_roots_endpoint(request: FindRootsRequest):
    operation, func = resolve_operation(
        request.operation,
        SOLVE_ROOTS,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/solve/roots",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/calculus/derivative")
def find_derivative_endpoint(request: FindDerivativeRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_DERIVATIVE,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
        request.order
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/calculus/derivative",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/calculus/integral")
def find_integral_endpoint(request: FindIntegralRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_INTEGRAL,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
        request.lower_bound,
        request.upper_bound,
    )

    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/calculus/integral",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/calculus/limit")
def find_limit_endpoint(request: FindLimitRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_LIMIT,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
        request.value
    )

    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/calculus/limit",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/function/domain")
def find_domain_endpoint(request: FindDomainRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_DOMAIN,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
        request.math_set
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/function/domain",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )

    return {'result': result}

@router.post("/function/intercepts")
def find_intercepts_endpoint(request: FindInterceptsRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_INTERCEPTS,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/function/intercepts",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/function/critical-points")
def find_critical_points_endpoint(request: FindCriticalPointsRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_CRIT_POINTS,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/function/critical-points",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}

@router.post("/function/inflection-points")
def find_inflection_points_endpoint(request: FindInflectionPointsRequest):
    operation, func = resolve_operation(
        request.operation,
        FIND_INFLECTIONS,
        'expression',
    )
    result = safe_execute(
        func,
        request.expr,
        request.variable,
        request.epsilon
    )
    result = serialize_result(result)
    state.add_to_history(
        endpoint="/expression/function/inflection-points",
        request_data=request.model_dump(),
        display_name=f" find {operation} ",
        output=result
    )
    return {'result': result}