import math
import numpy as np


# HELPERS

def to_vector(v) -> np.ndarray:
    """Convert input into a NumPy float vector."""
    return np.array(v, dtype=float)


def to_matrix(m) -> np.ndarray:
    """Convert input into a NumPy float matrix."""
    return np.array(m, dtype=float)


def validate_shapes(a, b):
    """Validate that two vectors/matrices have matching shapes."""
    if a.shape != b.shape:
        raise ValueError("Inputs must have the same shape")


# VECTOR OPERATIONS

def vector_add(v1, v2) -> list:
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    validate_shapes(v1, v2)
    return np.add(v1, v2).tolist()


def vector_subtract(v1, v2) -> list:
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    validate_shapes(v1, v2)
    return np.subtract(v1, v2).tolist()


def vector_magnitude(v) -> float:
    """
    Return the magnitude (Euclidean norm) of a vector.

    Example:
        [3, 4] -> 5
    """
    v = to_vector(v)
    return float(np.linalg.norm(v))


def vector_dot_product(v1, v2) -> float:
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    validate_shapes(v1, v2)
    return float(np.dot(v1, v2))


def vector_cross_product(v1, v2) -> list:
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    return np.cross(v1, v2).tolist()


def vector_scalar_multiply(v, scalar) -> list:
    v = to_vector(v)
    return np.multiply(v, scalar).tolist()


def vector_unit(v) -> list:
    v = to_vector(v)

    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("Zero vector has no unit vector")

    return (v / norm).tolist()


# MATRIX OPERATIONS

def matrix_add(m1, m2) -> list:
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    validate_shapes(m1, m2)
    return np.add(m1, m2).tolist()


def matrix_subtract(m1, m2) -> list:
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    validate_shapes(m1, m2)
    return np.subtract(m1, m2).tolist()


def matrix_scalar_multiply(m, scalar) -> list:
    m = to_matrix(m)
    return np.multiply(m, scalar).tolist()


def matrix_transpose(m) -> list:
    m = to_matrix(m)
    return np.transpose(m).tolist()


def matrix_multiply(m1, m2) -> list:
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    return np.matmul(m1, m2).tolist()



# MATRIX PROPERTIES

def matrix_determinant(m) -> float:
    m = to_matrix(m)
    return float(np.linalg.det(m))


def matrix_inverse(m) -> list:
    """
    Return the inverse of a square matrix.

    Raises:
        ValueError if matrix is singular.
    """
    m = to_matrix(m)

    try:
        return np.linalg.inv(m).tolist()
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is singular and cannot be inverted")


def matrix_trace(m) -> float:
    m = to_matrix(m)
    return float(np.trace(m))


def matrix_rank(m) -> int:
    m = to_matrix(m)
    return int(np.linalg.matrix_rank(m))



# LINEAR SYSTEMS

def solve_linear_system(a, b) -> list:
    """
    Solve Ax = b for x.

    Args:
        a:
            Square coefficient matrix
        b:
            Constant vector

    Returns:
        Solution vector

    Raises:
        ValueError:
            If matrix is not square or system has no unique solution.
    """
    a = to_matrix(a)
    b = to_vector(b)

    if a.shape[0] != a.shape[1]:
        raise ValueError("Coefficient matrix must be square")

    if a.shape[0] != len(b):
        raise ValueError("Matrix rows must match vector size")

    try:
        solution = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        raise ValueError("System has no unique solution")

    return solution.tolist()



# ADVANCED MATRIX OPS

def matrix_eigenvalues(m) -> list:
    """
    Return eigenvalues of a matrix.
    """
    m = to_matrix(m)
    return np.linalg.eigvals(m).tolist()


def matrix_eigenvectors(m) -> list:
    """
    Return eigenvectors of a matrix.
    """
    m = to_matrix(m)
    _, eigenvectors = np.linalg.eig(m)
    return eigenvectors.tolist()


def matrix_svd(m) -> dict:
    """
    Compute Singular Value Decomposition.

    Decomposes matrix A into:

        A = U * S * Vᵀ
    """
    m = to_matrix(m)
    u, s, vt = np.linalg.svd(m)

    return {
        "U": u.tolist(),
        "S": s.tolist(),
        "Vt": vt.tolist()
    }