from fastapi import APIRouter
from pydantic import BaseModel
import state
from services import plot
from utils.api_helpers import execute_and_log

router = APIRouter(
    prefix="/plot",
    tags=["Plotting"]
)

FUNCTION_PLOT_FUNCTIONS = {
    "function": plot.plot_function,
    "critical_points": plot.plot_critical_points,
    "extrema": plot.plot_extrema,
    "inflections": plot.plot_inflections,
}

DATASET_PLOT_FUNCTIONS = {
    "histogram": plot.plot_histogram,
    "boxplot": plot.plot_boxplot,
}

SCATTER_FUNCTIONS = {
    "scatter": plot.plot_scatterplot,
}

VECTOR_FUNCTIONS = {
    "vectors": plot.plot_vectors,
}

class FunctionPlotRequest(BaseModel):
    operation: str
    expr: str
    variable: str

class DatasetPlotRequest(BaseModel):
    operation: str
    data: list[float]

class ScatterPlotRequest(BaseModel):
    operation: str
    x_data: list[float]
    y_data: list[float]

class VectorPlotRequest(BaseModel):
    operation: str
    vector_list: list[list[float]]

@router.post("/function")
def function_plot_endpoint(request: FunctionPlotRequest):
    _, result = execute_and_log(
        "/plot/function",
        request,
        FUNCTION_PLOT_FUNCTIONS,
        "Plot",
        request.expr,
        request.variable,
        state.settings
    )

    return {"result": result}

@router.post("/dataset")
def dataset_plot_endpoint(request: DatasetPlotRequest):
    _, result = execute_and_log(
        "/plot/dataset",
        request,
        DATASET_PLOT_FUNCTIONS,
        "Plot",
        request.data,
        state.settings
    )
    return {"result": result}

@router.post("/scatter")
def scatter_plot_endpoint(request: ScatterPlotRequest):
    _, result = execute_and_log(
        "/plot/scatter",
        request,
        SCATTER_FUNCTIONS,
        "Plot",
        request.x_data,
        request.y_data,
        state.settings
    )

    return {"result": result}

@router.post("/vectors")
def vector_plot_endpoint(request: VectorPlotRequest):
    _, result = execute_and_log(
        "/plot/vectors",
        request,
        VECTOR_FUNCTIONS,
        "Plot",
        request.vector_list,
        state.settings
    )

    return {"result": result}