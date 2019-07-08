import numpy as np


def SkewSymmetricExpansion(vector):
    # Takes a vector and returns the Skew-Symmetric matrix expansion
    x1 = vector[0]
    x2 = vector[1]
    x3 = vector[2]
    return np.array([ [0.0, -x3, x2], [x3, 0.0, -x1], [-x2, x1, 0]])
