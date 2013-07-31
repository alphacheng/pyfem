import numpy
from numpy import ndarray as mat
from numpy import ndarray as vec
from numpy import eye
from numpy import array
from numpy import cross
from numpy import concatenate
from numpy.linalg import det
from numpy.linalg import inv
from numpy.linalg import pinv
from numpy.linalg import norm

numpy.set_printoptions(precision=8)

def tensor2(): return zeros(6)
def tensor4(): return zeros((6,6))

def mul(*args):
    """Multiplies matrices sequentialy A*B*C*..."""
    return reduce(numpy.dot, args)

def dott(left, rigth):
    """Matrices dot product"""
    return left*rigth #Just for numpy arrays

def zeros(*args):
    if len(args)==1: 
        return numpy.zeros(args[0])
    rows = args[0]
    cols = args[1]
    return numpy.zeros((rows,cols))

def empty(*args):
    if len(args)==1: 
        return numpy.empty(args[0])
    rows = args[0]
    cols = args[1]
    return numpy.empty((rows,cols))

def as_col(arr_1d):
    assert arr_1d.ndim == 1
    return arr_1d[numpy.newaxis].T

def as_row(arr_1d):
    assert arr_1d.ndim == 1
    return arr_1d[numpy.newaxis]

# Pseudo determinant of non-square matrices
def pdet(J):
    r = J.shape[0]
    c = J.shape[1]
    if r==2 and c==3:
        j1 = J[0,0]*J[1,1] - J[0,1]*J[1,0]
        j2 = J[0,1]*J[1,2] - J[0,2]*J[1,1]
        j3 = J[0,2]*J[1,0] - J[0,0]*J[1,2]
        return (j1*j1 + j2*j2 + j3*j3)**0.5  # jacobian determinant
    if r==1: return norm(J)
    if c==r: return det(J)
    raise Exception("Pseudo determinant: No rule to operate non-square matrix jacobian")
