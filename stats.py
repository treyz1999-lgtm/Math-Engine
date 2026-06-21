import math

import numpy as np
import statistics
import itertools

import scipy
from scipy import stats

from scipy import stats


def to_array(data):
    return np.array(data, dtype=float)

def validate_array(data):
    if data is None:
        raise ValueError("Data cannot be empty")

    try:
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
    except TypeError:
        raise ValueError("Data must be iterable")


#Descriptive statistics
def stats_mean(data):
    return statistics.mean(data)


def stats_median(data):
    return statistics.median(data)



def stats_mode(data):
    return statistics.mode(data)



def stats_range(data):
    validate_array(data)
    data = to_array(data)
    return np.max(data) - np.min(data)


def stats_variance(data, x):
    validate_array(data)
    data = to_array(data)
    return np.var(data, x)


def stats_std(data, x):
    validate_array(data)
    data = to_array(data)
    return np.std(data, x)



#Distribution / percentiles
def stats_percentile(data, p):
    validate_array(data)# we are not going to implement interpolation strategy input at this time as most do not need this
    data = to_array(data)

    if p < 0 or p > 100:
        raise ValueError("Percentile value must be between 0 and 100")

    return np.percentile(data, p)

def stats_quartiles(data):
    validate_array(data)
    data = to_array(data)
    return np.percentile(data, [25, 50, 75]).tolist()


def stats_iqr(data):
    validate_array(data)
    data = to_array(data)
    return stats.iqr(data)



#Relationship stats
def stats_covariance(x, y):
    validate_array(x)
    validate_array(y)
    if len(x) != len(y):
        raise ValueError("Arrays must have same length")
    return statistics.covariance(x, y)


def stats_correlation(x, y, ): #depending on the distribution we would want to use a different method, pearsonr will handle normal distributions
    coefficient, p_value = stats.pearsonr(x, y)
    if len(x) != len(y):
        raise ValueError("Arrays must have same length")
    return {
        'coefficient': coefficient,
        'p_value': p_value,
    }



#Others
def stats_permutations(n, r):
    validate_array(n)
    return math.perm(n, r)


def stats_combinations(n, r):
    validate_array(n)
    return math.comb(n, r)


def stats_z_score(x, mean, std):

    if std == 0:
        raise ValueError("Std cannot be zero")
    z = ( x - mean) / std

    return z