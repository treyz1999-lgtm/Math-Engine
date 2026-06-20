import math
import numpy as np

#HELPERS
def to_vector(v):
    return np.array(v, dtype=float)

def to_matrix(m):
    return np.array(m, dtype=float)

def validate_vector(v1, v2):
    if v1.shape != v2.shape:
        raise TypeError("vector must have the same shape")

# VECTOR
def vector_add(v1, v2):
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    validate_vector(v1, v2)
    return np.add(v1, v2).tolist()

def vector_subtract(v1, v2):
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    validate_vector(v1, v2)
    return np.subtract(v1, v2).tolist()


def vector_magnitude: #this will only support 1d vectors for the purposes of this project. Later implementations might allow for multidimensional arrays


def vector_dot_product:


def vector_cross_product:


def vector_scalar_multiply:


def vector_unit:



# MATRIX
def matrix_add:


def matrix_subtract:


def matrix_scalar_multiply:


def matrix_transpose:


def matrix_multiply:



# MATRIX PROPERTIES
def matrix_determinant:


def matrix_inverse:


def matrix_trace:


def matrix_rank:



# SYSTEMS
solve_linear_system:

#Matrix Properties
def matrix_eigenvalues(matrix):


def matrix_eigenvectors(matrix):


def matrix_svd(matrix):


def matrix_projection(v, onto):