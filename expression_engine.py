
import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)


#helpers
transformations = (
    standard_transformations +
    (implicit_multiplication_application,)
) #this allows SymPy to interpret strings how we might normally code them, but also allows for implicit multiplication i.e. how you learned it in school. Because we do not naturally use * for multiplication

def to_sympy(expr: str):
    """
    Convert a user-provided mathematical expression string into a SymPy expression.

    This helper normalizes user-friendly math syntax before parsing:
    - Replaces '^' with '**' for exponent notation
    - Supports implicit multiplication such as:
        2x -> 2*x
        2(x+1) -> 2*(x+1)
        (x+2)(x-2) -> (x+2)*(x-2)

    Examples:
        "x^2 + 3x"
        "(x+2)(x-2)"

    Args:
        expr (str):
            Mathematical expression entered by the user.

    Returns:
        SymPy expression object.

    Raises:
        ValueError:
            If the expression cannot be parsed.
    """
    expr = expr.replace("^", "**")

    try:
        return parse_expr(expr, transformations=transformations)
    except Exception:
        raise ValueError("Invalid mathematical expression")


def substitute_variables(expression, variables: dict | None = None):
    """
       Substitute numeric values into a symbolic SymPy expression.

       This function assumes the controller layer has already:
       1. Inspected expression.free_symbols
       2. Asked the user for all required variable values
       3. Built a variable dictionary such as:
          {"x": 3, "y": 4}

       This function validates that all required variables are present
       before performing substitution.

       Example:
           Expression: 2*x + y
           Variables: {"x": 3, "y": 4}
           Result: 10

       Args:
           expression:
               SymPy expression object.

           variables (dict | None):
               Dictionary mapping variable names to numeric values.

       Returns:
           SymPy expression with variables substituted.

       Raises:
           ValueError:
               If required variables are missing.
       """
    required_variables = {str(var) for var in expression.free_symbols}
    if not required_variables:
        return expression

    if not variables:
        raise ValueError(
            f"Expression requires variables: {required_variables}"
        )

    provided_variables = set(variables.keys())

    missing = required_variables - provided_variables
    if missing:
        raise ValueError(f"Missing required variables: {missing}")

    return expression.subs(variables)

#Expression manipulation

def evaluate_expression(expr: str, variables: dict | None = None):
    """
    Evaluate a mathematical expression numerically.

    Converts a user-provided expression string into a SymPy expression,
    substitutes numeric values for all required variables, and returns
    the final evaluated result as a float.

    Examples:
        expr = "2*x + y"
        variables = {"x": 3, "y": 4}
        Result -> 10.0

    :param expr: str
        Mathematical expression entered by the user.

    :param variables: dict | None
        Dictionary mapping variable names to numeric values.
        Example: {"x": 3, "y": 4}

    :return: float
        Numeric result after substitution and evaluation.

    :raises ValueError:
        Raised if the expression is invalid or required variables are missing.
    """
    expression = to_sympy(expr)
    expression = substitute_variables(expression, variables)
    return float(expression.evalf())

def simplify_expression(expr: str):
    """
    Simplify a symbolic mathematical expression.

    Converts a user-provided expression string into a SymPy expression
    and simplifies it algebraically.

    Example:
        "2*x + 3*x" -> 5*x

    :param expr: str
        Mathematical expression entered by the user.

    :return: SymPy expression object
        Simplified symbolic expression.
    """
    expression = to_sympy(expr)
    simplified_expression = sp.simplify(expression)
    return simplified_expression

def expand_expression(expr: str):
    """
    Expand a symbolic mathematical expression.

    Converts a user-provided expression string into a SymPy expression
    and expands products or powers into expanded polynomial form.

    Example:
        "(x+2)*(x-2)" -> x**2 - 4

    :param expr: str
        Mathematical expression entered by the user.

    :return: SymPy expression object
        Expanded symbolic expression.
    """
    expression = to_sympy(expr)
    expanded_expression = sp.expand(expression)
    return expanded_expression


def factor_expression(expr: str):
    """
    Factor a symbolic mathematical expression.

    Converts a user-provided expression string into a SymPy expression
    and factors it into simpler multiplicative components.

    Example:
        "x**2 - 4" -> (x - 2)*(x + 2)


    :param expr: str
        Mathematical expression entered by the user.

    :return: SymPy expression object
        Factored symbolic expression.
    """
    expression = to_sympy(expr)
    factored_expression = sp.factor(expression)
    return factored_expression


#Equation solving

def solve_linear_equation(left_hand_side: str, right_hand_side : str, variable : str):
    """
      Solve a linear equation for a single variable.

      Example:
          2*x + 3 = 13

      Args:
          left_hand_side (str):
              Left-hand side of the equation.

          right_hand_side (str):
              Right-hand side of the equation.

          variable (str):
              Variable to solve for.

      Returns:
          list:
              List of solution values.

              Examples:
                  [5]      -> one solution
                  []       -> no solution
      """

    left_expression = to_sympy(left_hand_side)
    right_expression = to_sympy(right_hand_side)
    solve_for = sp.Symbol(variable)

    solutions = sp.solve([left_expression, right_expression], solve_for)

    if not solutions:
        raise ValueError('No solutions found')

    return solutions

def solve_quadratic(a: float, b: float, c: float):
    """
       Solve a quadratic equation of the form:

           ax² + bx + c = 0

       The function constructs the quadratic expression using the
       provided coefficients and solves for x using SymPy.

       Example:
           a = 1, b = -5, c = 6

           x² - 5x + 6 = 0

           Returns:
               [2, 3]

       Args:
           a (float):
               Coefficient of x². Must not be zero.

           b (float):
               Coefficient of x.

           c (float):
               Constant term.

       Returns:
           list:
               List of real or complex roots.

               Examples:
                   [5]        -> one repeated root
                   [2, 3]     -> two distinct roots
                   [-I, I]    -> complex roots

       Raises:
           ValueError:
               If coefficient 'a' is zero.
       """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation")

    x = sp.Symbol("x")
    expression = a*x**2 + b*x + c
    return sp.solve(expression, x)

def solve_equation(lhs: str, rhs: str, variable: str):
    """
       Solve a system of equations for one or more variables.

       Each equation should be provided as a string expression already
       rearranged into standard form where the equation equals zero.

       Example system:
           x + y = 5
           x - y = 1

       Should be passed as:
           equations = ["x + y - 5", "x - y - 1"]
           variables = ["x", "y"]

       The function converts each equation into a SymPy expression,
       converts each variable name into a SymPy Symbol, and uses
       SymPy's solve() method to solve the system.

       Args:
           equations (list):
               List of equation strings in standard form.

           variables (list):
               List of variable names to solve for.

       Returns:
           list[dict]:
               List of solution dictionaries mapping variables to values.

               Example:
                   [{x: 3, y: 2}]

               Multiple solutions may return multiple dictionaries:
                   [
                       {x: 1, y: 2},
                       {x: -1, y: 2}
                   ]

               No solutions return:
                   []

       Raises:
           ValueError:
               Raised if an equation cannot be parsed.
       """
    lhs = to_sympy(lhs)
    rhs = to_sympy(rhs)
    variable = sp.Symbol(variable)
    if variable not in lhs.free_symbols.union(rhs.free_symbols):
        raise ValueError(f"Variable '{variable}' not found in equation")

    equation = lhs - rhs

    return sp.solve(equation, variable)

def solve_system(equations : list[str], variables : list[str]):
    equations = [to_sympy(eq) for eq in equations]

    variables = [sp.Symbol(var) for var in variables]

    solutions = sp.solve(equations, variables, dict=True)
    return solutions



#Polynomials
def find_roots(expression: str, variable: str):
    """
        Find the roots (zeros) of a polynomial or symbolic expression.

        A root is a value of the chosen variable that makes the
        expression equal to zero.

        Example:
            x^2 - 5x + 6 = 0

            Returns:
                [2, 3]

        Args:
            expression (str):
                Mathematical expression entered by the user.

            variable (str):
                Variable to solve for.

        Returns:
            list:
                List of roots (real or complex).

                Examples:
                    [5]
                    [2, 3]
                    [-I, I]
        """
    expression = to_sympy(expression)
    variable = sp.Symbol(variable)

    return sp.solve(expression, variable)

def derivative(expression: str, variable: str, order: int):
    """
        Compute the symbolic derivative of an expression with respect to a chosen variable.

        The function converts a user-provided mathematical expression into a
        SymPy expression and computes its derivative using SymPy's diff() method.
        Higher-order derivatives are supported by specifying the derivative order.

        Examples:
            expression = "x^3 + 2*x"
            variable = "x"
            order = 1

            Returns:
                3*x**2 + 2

            expression = "x^3"
            variable = "x"
            order = 2

            Returns:
                6*x

        Args:
            expression (str):
                Mathematical expression entered by the user.

            variable (str):
                Variable to differentiate with respect to.

            order (int):
                Order of the derivative.
                Example:
                    1 -> first derivative
                    2 -> second derivative
                    3 -> third derivative

        Returns:
            SymPy expression object:
                Symbolic derivative of the expression.
        """
    if order < 1:
        raise ValueError("Derivative order must be at least 1")
    expression = to_sympy(expression)
    variable = sp.Symbol(variable)
    return sp.diff(expression, variable, order)


def integral(expression: str, variable: str, a=None, b=None):
    """
       Compute the symbolic or definite integral of an expression.

       The function converts a user-provided mathematical expression into a
       SymPy expression and computes either:

       - An indefinite integral if no bounds are provided
       - A definite integral if both lower and upper bounds are provided

       Examples:
           Indefinite integral:
               expression = "x^2"
               variable = "x"

               Returns:
                   x**3 / 3

           Definite integral:
               expression = "x^2"
               variable = "x"
               a = 0
               b = 3

               Returns:
                   9

       Args:
           expression (str):
               Mathematical expression entered by the user.

           variable (str):
               Variable to integrate with respect to.

           a (int | float | str | None):
               Lower bound of integration.
               If None, the integral is treated as indefinite.

           b (int | float | str | None):
               Upper bound of integration.
               Must be provided together with a for definite integrals.

       Returns:
           SymPy expression object | numeric value:
               - Returns a symbolic expression for indefinite integrals
               - Returns a numeric or symbolic result for definite integrals

       Raises:
           ValueError:
               Raised if only one bound is provided.
       """
    expression = to_sympy(expression)
    variable = sp.Symbol(variable)

    # Indefinite integral
    if a is None and b is None:
        return sp.integrate(expression, variable)

    # Require both bounds for definite integral
    if a is None or b is None:
        raise ValueError("Both lower and upper bounds are required")

    a = to_sympy(str(a))
    b = to_sympy(str(b))

    return sp.integrate(expression, (variable, a, b))


def limit(expr, variable, value):
    """
        Compute the limit of an expression as a variable approaches a given value.

        The function converts a user-provided mathematical expression into a
        SymPy expression and evaluates its limit with respect to the chosen variable.

        Examples:
            expr = "sin(x)/x"
            variable = "x"
            value = 0

            Returns:
                1

            expr = "1/x"
            variable = "x"
            value = "oo"

            Returns:
                0

        Args:
            expr (str):
                Mathematical expression entered by the user.

            variable (str):
                Variable approaching the specified value.

            value (int | float | str):
                Value that the variable approaches.

                Examples:
                    0
                    2
                    "pi"
                    "oo"   (positive infinity)
                    "-oo"  (negative infinity)

        Returns:
            SymPy expression object | numeric value:
                Result of the evaluated limit.

        Raises:
            ValueError:
                Raised if the expression or limit value cannot be parsed.
        """
    expression = to_sympy(expr)
    symbol = sp.Symbol(variable)
    value = to_sympy(str(value))
    return sp.limit(expression, symbol, value)


#Function analysis
def function_domain(expr: str, variable: str, math_set=None):
    """
       Determine the domain of a mathematical function over a specified set.

       The function converts a user-provided mathematical expression into a
       SymPy expression and determines where the function is defined and
       continuous with respect to the chosen variable.

       If no mathematical set is provided, the function defaults to the
       real numbers.

       Examples:
           expr = "1/x"
           variable = "x"
           math_set = "Reals"

           Returns:
               Union(Interval.open(-oo, 0), Interval.open(0, oo))

           expr = "sqrt(x)"
           variable = "x"

           Returns:
               Interval(0, oo)

       Args:
           expr (str):
               Mathematical expression entered by the user.

           variable (str):
               Variable to analyze the domain with respect to.

           math_set (str | None):
               Mathematical set used as the search space.

               Supported sets:
                   "Reals"
                   "Complexes"
                   "Integers"
                   "Naturals"
                   "Naturals0"

               Defaults to Reals if not provided.

       Returns:
           SymPy set object:
               Domain where the function is defined and continuous.

       Raises:
           ValueError:
               Raised if an unsupported mathematical set is provided.
       """
    expression = to_sympy(expr)
    variable = sp.Symbol(variable)

    allowed_sets = {
        "reals": sp.S.Reals,
        "complexes": sp.S.Complexes,
        "integers": sp.S.Integers,
        "naturals": sp.S.Naturals,
        "naturals0": sp.S.Naturals0
    }

    if math_set is None:
        domain_set = sp.S.Reals
    else:
        math_set = math_set.lower().strip()

        if math_set not in allowed_sets:
            raise ValueError(
                f"Math set must be one of: {tuple(allowed_sets.keys())}"
            )

        domain_set = allowed_sets[math_set]

    return continuous_domain(expression, variable, domain_set)


def function_intercepts(expr: str):
    """
       Determine the x-intercepts and y-intercept of a single-variable function.

       The function converts a user-provided mathematical expression into a
       SymPy expression, automatically detects its variable, and computes:

       - x-intercepts by solving f(x) = 0
       - y-intercept by evaluating the function at x = 0

       The expression must contain exactly one variable.

       Examples:
           expr = "x^2 - 4*x + 3"

           Returns:
               {
                   "x_intercepts": [(1, 0), (3, 0)],
                   "y_intercept": (0, 3)
               }

           expr = "t^2 - 9"

           Returns:
               {
                   "x_intercepts": [(-3, 0), (3, 0)],
                   "y_intercept": (0, -9)
               }

       Args:
           expr (str):
               Mathematical expression entered by the user.

               Example:
                   "x^2 - 4*x + 3"
                   "sin(t)"
                   "1/x"

       Returns:
           dict:
               Dictionary containing the x-intercepts and y-intercept.

               Structure:
                   {
                       "x_intercepts": list[tuple],
                       "y_intercept": tuple
                   }

       Raises:
           ValueError:
               Raised if the expression contains zero or multiple variables.

           ZeroDivisionError:
               Raised if the function is undefined at x = 0,
               meaning no y-intercept exists.
       """
    expression = to_sympy(expr)

    variables = expression.free_symbols

    if len(variables) != 1:
        raise ValueError(
            "Expression must contain exactly one variable"
        )

    variable = next(iter(variables))

    y_value = expression.subs(variable, 0)

    if not y_value.is_finite:
        raise ValueError(
            "Function is undefined at 0, no y-intercept exists"
        )

    y_intercept = (0, y_value)

    x_values = sp.solve(expression, variable)
    x_intercepts = [(value, 0) for value in x_values]

    return {
        "x_intercepts": x_intercepts,
        "y_intercept": y_intercept
    }

def critical_points(expr, variable):
    """
       Determine the critical points of a single-variable function.

       A critical point occurs where the first derivative of a function
       equals zero. This function computes the first derivative, solves
       for all x-values where f'(x) = 0, and returns the corresponding
       coordinate points on the original function.

       Note:
           This implementation only identifies critical points where
           the derivative equals zero. It does not currently detect
           points where the derivative is undefined.

       Examples:
           expr = "x^2 - 4*x + 3"
           variable = "x"

           Derivative:
               2*x - 4

           Critical point:
               x = 2

           Returns:
               [(2, -1)]

       Args:
           expr (str):
               Mathematical expression entered by the user.

               Example:
                   "x^2 - 4*x + 3"
                   "sin(x)"
                   "x^3 - 3*x"

           variable (str):
               Variable to differentiate with respect to.

       Returns:
           list[tuple]:
               List of coordinate tuples representing critical points.

               Example:
                   [(2, -1)]
                   [(0, 0), (2, 4)]

       Raises:
           ValueError:
               Raised if the expression does not contain the
               specified variable.
       """
    expression = to_sympy(expr)
    variable = sp.Symbol(variable)
    if variable not in expression.free_symbols:
        raise ValueError(
            "Expression must contain the specified variable"
        )
    prime = sp.diff(expression, variable )
    crit_points = sp.solve(prime, variable)
    coordinates = [
        (x_val, expression.subs(variable, x_val))
        for x_val in crit_points
    ]

    return coordinates

def local_extrema(expr : str, variable : str):
    """
        Determine the local extrema of a single-variable function using
        the second derivative test.

        The function first finds all critical points of the expression,
        then computes the second derivative and evaluates it at each
        critical x-value to classify the point as:

        - Local minimum if f''(x) > 0
        - Local maximum if f''(x) < 0
        - Inconclusive if f''(x) = 0

        Note:
            This implementation assumes real-valued functions and only
            analyzes critical points where the first derivative equals zero.
            It does not currently detect extrema at points where the
            derivative is undefined.

        Examples:
            expr = "x^2 - 4*x + 3"
            variable = "x"

            Critical point:
                (2, -1)

            Second derivative:
                2

            Since 2 > 0:
                Local minimum

            Returns:
                [(2, -1, "minimum")]

        Args:
            expr (str):
                Mathematical expression entered by the user.

                Example:
                    "x^2 - 4*x + 3"
                    "x^3 - 3*x"
                    "sin(x)"

            variable (str):
                Variable used for differentiation.

        Returns:
            list[tuple]:
                List of tuples containing:
                    (x-coordinate, y-coordinate, classification)

                Classification will be one of:
                    "minimum"
                    "maximum"
                    "inconclusive"

                Example:
                    [
                        (-1, 2, "maximum"),
                        (1, -2, "minimum")
                    ]

        Raises:
            ValueError:
                Raised if the expression does not contain the
                specified variable.
        """
    expression = to_sympy(expr)
    variable = sp.Symbol(variable)

    second_derivative = sp.diff(expression, variable, 2)
    points = critical_points(expr, str(variable))

    extrema = []

    for x_val, y_val in points:

        second_value = second_derivative.subs(variable, x_val)

        if second_value > 0:
            extrema.append((x_val, y_val, "local minimum"))
        elif second_value < 0:
            extrema.append((x_val, y_val, "local maximum"))
        else:
            extrema.append((x_val, y_val, "inconclusive"))

    return extrema

def inflection_points(expr: str,variable: str,epsilon: float | None = None):
    """
      Determine the inflection points of a single-variable function.

      An inflection point occurs where the function changes concavity,
      meaning the second derivative changes sign from positive to negative
      or from negative to positive.

      This function:
      1. Computes the second derivative of the expression
      2. Solves for candidate points where f''(x) = 0
      3. Tests a small distance to the left and right of each candidate
         to determine whether the second derivative changes sign
      4. Returns the coordinates of all confirmed inflection points

      The sign-change test uses a small epsilon value to sample nearby
      points around each candidate.

      Examples:
          expr = "x^3"
          variable = "x"

          Second derivative:
              6*x

          Candidate:
              x = 0

          Left side (x = -0.1):
              negative

          Right side (x = 0.1):
              positive

          Since the sign changes:
              (0, 0) is an inflection point

          Returns:
              [(0, 0)]

      Args:
          expr (str):
              Mathematical expression entered by the user.

              Example:
                  "x^3"
                  "x^4"
                  "sin(x)"

          variable (str):
              Variable used for differentiation.

          epsilon (float | None):
              Small positive value used to sample points to the
              left and right of each candidate inflection point.

              Defaults to 0.1 if not provided.

      Returns:
          list[tuple]:
              List of coordinate tuples representing inflection points.

              Example:
                  [(0, 0)]
                  [(-2, 5), (3, -1)]

      Raises:
          ValueError:
              Raised if epsilon is not numeric or is less than
              or equal to zero.
      """
    expression = to_sympy(expr)
    variable = sp.Symbol(variable)

    if epsilon is None:
        epsilon = 0.1

    try:
        epsilon = float(epsilon)
    except:
        raise ValueError("epsilon must be numeric")

    if epsilon <= 0:
        raise ValueError("epsilon must be greater than 0")

    if epsilon <= 0:
        raise ValueError("epsilon must be greater than 0")

    points = []
    second_derivative = sp.diff(expression, variable, 2)
    candidates = sp.solve(second_derivative, variable)

    for candidate in candidates:
        if candidate.is_real:
            left = second_derivative.subs(variable, candidate - epsilon)
            right = second_derivative.subs(variable, candidate + epsilon)

            if left * right < 0:
                y_value = expression.subs(variable, candidate)
                points.append((candidate, y_value))

    return points
