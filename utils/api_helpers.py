from fastapi import  HTTPException
import  state

def resolve_operation(operation: str, function_map: dict,):
    """
    Normalize an operation string and resolve its mapped function.

    This helper is used by API endpoints that support multiple operations
    through a single route. It converts the user-provided operation to
    lowercase, looks up the corresponding function in a dispatch map,
    and returns both the normalized operation and function reference.

    Example:
        function_map = {
            "sin": trig.trig_sin,
            "cos": trig.trig_cos
        }

        Input:
            operation = "SIN"

        Output:
            ("sin", trig.trig_sin)

    Args:
        operation (str):
            Operation name provided by the request payload.

            Example:
                "sin"
                "solve_side"
                "matrix_inverse"

        function_map (dict):
            Dictionary mapping operation names to function references.

            Example:
                {
                    "sin": trig.trig_sin,
                    "cos": trig.trig_cos
                }

        family (str):
            Name of the operation group used for error messaging.

            Example:
                "trig"
                "linear algebra"
                "calculus"

    Returns:
        tuple[str, callable]:
            A tuple containing:
                - normalized operation string
                - resolved function reference

    Raises:
        HTTPException:
            Status code 400 if the operation is invalid or not found
            in the provided function map.
    """
    operation = operation.lower()
    func = function_map.get(operation)

    if func is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid operation"
        )

    return operation, func


def safe_execute(func, *args):
    """
      Execute a function safely and convert ValueErrors into HTTP errors.

      This helper wraps service-layer function calls so API routes do not
      need repetitive try/except blocks. Any ValueError raised by the
      underlying function is converted into an HTTP 400 response.

      The *args parameter allows this helper to accept an arbitrary number
      of positional arguments.

      Example:
          safe_execute(func, arg1)
          safe_execute(func, arg1, arg2)
          safe_execute(func, arg1, arg2, arg3, settings)

      How *args works:
          *args collects all extra positional arguments into a tuple.

          Example:
              safe_execute(func, 1, 2, 3)

          Inside the function:
              args == (1, 2, 3)

          When calling:
              func(*args)

          Python unpacks the tuple back into separate arguments:

              func(1, 2, 3)

      This is useful because calculator functions have different signatures.

      Examples:
          trig_sin(angle, settings)
          triangle_leg(hypotenuse, leg)
          law_of_sines(side, angle, target, settings)

      Using *args allows one helper to support all of them.

      Args:
          func:
              Function reference to execute.

          *args:
              Arbitrary positional arguments passed to func.

      Returns:
          The result returned by func.

      Raises:
          HTTPException:
              Status code 400 if func raises a ValueError.
      """
    try:
        return func(*args)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def serialize_result(result):
    """
    Convert non-JSON-friendly results into serializable values.

    FastAPI responses must be JSON serializable. Most basic Python types
    are already supported by JSON and can be returned unchanged.

    Supported JSON-friendly types include:
        - int
        - float
        - str
        - bool
        - list
        - dict

    Some calculator operations, especially from SymPy, return objects
    that JSON does not handle well.

    Examples of non-JSON-friendly objects:
        - SymPy expressions
        - Interval objects
        - Symbol objects
        - Matrix objects
        - custom classes

    For unsupported result types, this helper converts the object to a
    string representation so it can be safely returned in API responses
    and stored in history.

    Example:
        Input:
            Interval(0, oo)

        Output:
            "Interval(0, oo)"

    Args:
        result:
            Result returned by a service-layer function.

    Returns:
        JSON-serializable value:
            Returns the original result if already JSON-friendly,
            otherwise returns its string representation.
    """
    if result is None:
        return None
    if isinstance(result, (int, float, str, bool, list, dict)):
        return result
    return str(result)

def execute_and_log(endpoint, request, function_map, display_prefix, *args):
    """
        Resolve an operation, execute it safely, serialize the result,
        and store the completed request in calculator history.

        This helper removes repeated API route boilerplate by combining
        the most common calculator endpoint workflow into one reusable function.

        Common workflow steps:
            1. Resolve requested operation to a function reference
            2. Execute the function safely
            3. Convert result to a JSON-safe value
            4. Save request/response to history for replay
            5. Return operation name and serialized result

        This helper works best for route groups where all mapped operations
        share the same function signature (shape).

        Examples of compatible route groups:
            Basic trig:
                func(value, settings)

            Law of sines:
                func(side, angle, target, settings)

            Basic arithmetic:
                func(value1, value2)

        In these cases, every operation in the route can be called with
        the same argument structure, making this helper a good fit.

        When NOT to use this helper:
            Avoid using this helper when a route contains operations with
            different function signatures or special branching logic.

            Example:
                triangle_hypotenuse(a, b)
                triangle_leg(hypotenuse, leg)
                triangle_third_angle(angle1, angle2, settings)

            Since not all functions accept the same arguments, the route
            must decide which arguments to pass before execution.

            In those cases, writing the route manually is often clearer
            than forcing abstraction.

        Args:
            endpoint (str):
                API route string used for history replay.

            request:
                Pydantic request model instance.

            function_map (dict):
                Dictionary mapping operation names to function references.

            display_prefix (str):
                Human-readable label used in history display.

            *args:
                Positional arguments passed into the resolved function.

        Returns:
            tuple[str, Any]:
                A tuple containing:
                    - normalized operation string
                    - serialized result
    """
    operation, func = resolve_operation(
        request.operation,
        function_map
    )
    result = safe_execute(func, *args)
    result = serialize_result(result)

    state.add_to_history(
        endpoint=endpoint,
        request_data=request.model_dump(),
        display_name=f"{display_prefix}: {operation}",
        output=result
    )

    return operation, result