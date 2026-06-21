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


def vector_magnitude(v1, v2): #this will only support 1d vectors for the purposes of this project. Later implementations might allow for multidimensional arrays

    return math.sqrt(v1**2 + v2**2)

def vector_dot_product(v1, v2):
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    return np.dot(v1, v2).tolist()

def vector_cross_product(v1, v2):
    v1 = to_vector(v1)
    v2 = to_vector(v2)
    return np.cross(v1, v2).tolist()

def vector_scalar_multiply(v1, scalar):
    v1 = to_vector(v1)
    v1 *= scalar
    return v1


def vector_unit(v1):
    v1 = to_vector(v1)
    return v1/np.linalg.norm(v1)


# MATRIX
def matrix_add(m1, m2):
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    validate_vector(m1, m2)
    return np.add(m1, m2).tolist()

def matrix_subtract(m1, m2):
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    validate_vector(m1, m2)
    return np.subtract(m1, m2).tolist()


def matrix_scalar_multiply(m1, scalar):
    m1 = to_matrix(m1)
    return np.multiply(m1, scalar).tolist()


def matrix_transpose(m):
    return np.transpose(m).tolist()


def matrix_multiply(m1, m2):
    m1 = to_matrix(m1)
    m2 = to_matrix(m2)
    return np.matmul(m1, m2).tolist()



# MATRIX PROPERTIES
def matrix_determinant(m):
    m = to_matrix(m)
    return np.linalg.det(m)

def matrix_inverse(m):
    m = to_matrix(m)
    return np.linalg.inv(m)


def matrix_trace(m):
    m = to_matrix(m)
    return np.trace(m)


def matrix_rank(m):
    m = to_matrix(m)
    return np.linalg.matrix_rank(m)



# SYSTEMS
def solve_linear_system(a, b):
    a = to_matrix(a)
    b = to_matrix(b)
    if a.shape[0] != a.shape[1]:
        raise ValueError("Coefficient matrix must be square")

    if a.shape[0] != len(b):
        raise ValueError("Matrix rows must match vector size")

    try:
        solution = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        raise ValueError("System has no unique solution")

    return solution.tolist()


#Matrix Properties
def matrix_eigenvalues(m):# numpy has a method .linalg.eig() that will return eigenvalues and eigenvectors, but we will do each separately
    m = to_matrix(m)
    return np.linalg.eigvals(m)

def matrix_eigenvectors(m):# we might later just use 1 function to return both, but this allows for the user to get just the information they want. The downside being you would need to run the computation twice to get both
    m = to_matrix(m)
    eigenvalues, eigenvectors = np.linalg.eig(m)
    return eigenvectors


def matrix_svd(m):#this doesn't really belong in a 'calculator' most people will never know or use this
    m = to_matrix(m)
    u, s, vt = np.linalg.svd(m)
    return {
        'U' : u.tolist(),
        'S' : s.tolist(),
        'Vt' : vt.tolist()
    }

#def matrix_projection(v, onto):
