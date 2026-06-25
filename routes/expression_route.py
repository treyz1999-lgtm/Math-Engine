from fastapi import APIRouter
from pydantic import BaseModel
import state
from services import expression_engine as ex
from utils.api_helpers import execute_and_log

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

FIND_DOMAIN = {
    'domain' : ex.function_domain
}

FIND_INTERCEPTS = {
    'intercepts' : ex.function_intercepts
}

FIND_CRIT_POINTS = {
    'critical_points' : ex.critical_points,
    'local_extrema' : ex.local_extrema,
}

FIND_INFLECTIONS = {
    'inflection_points' : ex.inflection_points,
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

# ROUTES
@router.post("/manipulate")
def manipulate_expression_endpoint(request: ManipulateExpressionRequest):
    _, result = execute_and_log(
        "/expressions/manipulate",
        request,
        MANIPULATE_EXPRESSION,
        "expression",
        request.expr,
    )
    return {"result": result}


@router.post("/evaluate")
def evaluate_expression_endpoint(request: EvaluateExpressionRequest):
    _, result = execute_and_log(
        "/expressions/evaluate",
        request,
        EVALUATE_EXPRESSION,
        "expression",
        request.expr,
        request.variables,
    )
    return {"result": result}

@router.post("/solve/equation")
def solve_equation_endpoint(request: SolveEquationRequest):
    _, result = execute_and_log(
        "/expressions/solve/equation",
        request,
        SOLVE_EQUATION,
        "Solve",
        request.left_hand,
        request.right_hand,
        request.variable
    )
    return {"result": result}

@router.post("/solve/quadratic")
def solve_quadratic_endpoint(request: SolveQuadraticRequest):
    _, result = execute_and_log(
        "/expressions/solve/quadratic",
        request,
        SOLVE_QUADRATIC,
        "Solve",
        request.value1,
        request.value2,
        request.value3
    )
    return {"result": result}

@router.post("/solve/system")
def solve_system_endpoint(request: SolveSystemRequest):
    _, result = execute_and_log(
        "/expressions/solve/system",
        request,
        SOLVE_SYSTEM,
        "Solve",
        request.equations,
        request.variables
    )
    return {"result": result}

@router.post("/solve/roots")
def solve_roots_endpoint(request: FindRootsRequest):
    _, result = execute_and_log(
        "/expressions/solve/roots",
        request,
        SOLVE_ROOTS,
        "Find",
        request.expr,
        request.variable
    )
    return {"result": result}

@router.post("/calculus/derivative")
def find_derivative_endpoint(request: FindDerivativeRequest):
    _, result = execute_and_log(
        "/expressions/calculus/derivative",
        request,
        FIND_DERIVATIVE,
        "Find",
        request.expr,
        request.variable,
        request.order
    )
    return {"result": result}

@router.post("/calculus/integral")
def find_integral_endpoint(request: FindIntegralRequest):
    _, result = execute_and_log(
        "/expressions/calculus/integral",
        request,
        FIND_INTEGRAL,
        "Find",
        request.expr,
        request.variable,
        request.lower_bound,
        request.upper_bound
    )
    return {"result": result}

@router.post("/calculus/limit")
def find_limit_endpoint(request: FindLimitRequest):
    _, result = execute_and_log(
        "/expressions/calculus/limit",
        request,
        FIND_LIMIT,
        "Find",
        request.expr,
        request.variable,
        request.value
    )
    return {"result": result}

@router.post("/function/domain")
def find_domain_endpoint(request: FindDomainRequest):
    _, result = execute_and_log(
        "/expressions/function/domain",
        request,
        FIND_DOMAIN,
        "Find",
        request.expr,
        request.variable,
        request.math_set
    )
    return {"result": result}

@router.post("/function/intercepts")
def find_intercepts_endpoint(request: FindInterceptsRequest):
    _, result = execute_and_log(
        "/expressions/function/intercepts",
        request,
        FIND_INTERCEPTS,
        "Find",
        request.expr
    )
    return {"result": result}

@router.post("/function/critical-points")
def find_critical_points_endpoint(request: FindCriticalPointsRequest):
    _, result = execute_and_log(
        "/expressions/function/critical-points",
        request,
        FIND_CRIT_POINTS,
        "Find",
        request.expr,
        request.variable
    )
    return {"result": result}

@router.post("/function/inflection-points")
def find_inflection_points_endpoint(request: FindInflectionPointsRequest):
    _, result = execute_and_log(
        "/expressions/function/inflection-points",
        request,
        FIND_INFLECTIONS,
        "Find",
        request.expr,
        request.variable,
        state.settings["calculus"]["epsilon"]
    )
    return {"result": result}