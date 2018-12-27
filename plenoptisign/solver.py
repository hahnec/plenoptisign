from numpy import dot, transpose
from numpy.linalg import inv

def solve_sle(A, b):
    ''' function solver for system of linear equations '''

    if is_square(A):
        A_inv = inv(A)
    else:
        A_inv = pseudo_inv(A)

    return dot(A_inv, b)

def is_square(A):
    ''' check if matrix is square'''

    return all(len(row) == len(A) for row in A)

def pseudo_inv(A):
    ''' compute pseudo inverse '''

    return dot(transpose(A), inv(dot(A, transpose(A))))