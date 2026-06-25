import math
import numpy as np
import statistics
from scipy import stats


def to_array(data: list[float]) -> np.ndarray:
    return np.array(data, dtype=float)


def validate_array(data: list[float]) -> None:
    if data is None:
        raise ValueError("Data cannot be empty")

    try:
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
    except TypeError:
        raise ValueError("Data must be iterable")


# Descriptive statistics
def stats_mean(data: list[float]) -> float:
    return statistics.mean(data)


def stats_median(data: list[float]) -> float:
    return statistics.median(data)


def stats_mode(data: list[float]) -> float:
    return statistics.mode(data)


def stats_range(data: list[float]) -> float:
    validate_array(data)
    data = to_array(data)
    return np.max(data) - np.min(data)


def stats_variance(data: list[float], degrees_of_freedom: int) -> float:
    validate_array(data)
    data = to_array(data)
    return np.var(data, ddof=degrees_of_freedom)


def stats_std(data: list[float], degrees_of_freedom: int) -> float:
    validate_array(data)
    data = to_array(data)
    return np.std(data, ddof=degrees_of_freedom)


# Distribution / percentiles
def stats_percentile(data: list[float], percentile: float) -> float:
    validate_array(data)
    data = to_array(data)

    if percentile < 0 or percentile > 100:
        raise ValueError("Percentile must be between 0 and 100")

    return np.percentile(data, percentile)


def stats_quartiles(data: list[float]) -> list[float]:
    validate_array(data)
    data = to_array(data)
    return np.percentile(data, [25, 50, 75]).tolist()


def stats_iqr(data: list[float]) -> float:
    validate_array(data)
    data = to_array(data)
    return stats.iqr(data)


# Relationship statistics
def stats_covariance(
    dataset_1: list[float],
    dataset_2: list[float]
) -> float:
    validate_array(dataset_1)
    validate_array(dataset_2)

    if len(dataset_1) != len(dataset_2):
        raise ValueError("Arrays must have same length")

    return statistics.covariance(dataset_1, dataset_2)


def stats_correlation(
    dataset_1: list[float],
    dataset_2: list[float]
) -> dict:
    validate_array(dataset_1)
    validate_array(dataset_2)

    if len(dataset_1) != len(dataset_2):
        raise ValueError("Arrays must have same length")

    coefficient, p_value = stats.pearsonr(dataset_1, dataset_2)

    return {
        "coefficient": coefficient,
        "p_value": p_value,
    }


# Combinatorics
def stats_permutations(total_items: int, selected_items: int) -> int:
    if total_items < 0 or selected_items < 0:
        raise ValueError("Values must be non-negative")

    return math.perm(total_items, selected_items)


def stats_combinations(total_items: int, selected_items: int) -> int:
    if total_items < 0 or selected_items < 0:
        raise ValueError("Values must be non-negative")

    return math.comb(total_items, selected_items)


# Standard score
def stats_z_score(
    value: float,
    mean: float,
    standard_deviation: float
) -> float:
    if standard_deviation == 0:
        raise ValueError("Standard deviation cannot be zero")

    z_score = (value - mean) / standard_deviation
    return z_score