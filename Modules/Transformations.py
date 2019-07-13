import numpy as np
from Modules import Geodesy


def skewSymmetricExpansion(vector):
    # Takes a vector and returns the Skew-Symmetric matrix expansion
    x1 = np.asscalar(vector[0])
    x2 = np.asscalar(vector[1])
    x3 = np.asscalar(vector[2])
    return np.array([ [0.0, -x3, x2], [x3, 0.0, -x1], [-x2, x1, 0]])

def get_T_GI(lat,lon):
    sin_lat = np.sin(lat)
    cos_lat = np.cos(lon)
    sin_lon = np.sin(lon)
    cos_lon = np.cos(lon)
    return np.array([   [-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lon)],
                    [-np.sin(lon), np.cos(lon), 0.0],
                    [-np.cos(lat) * np.cos(lon), -np.cos(lon) * np.sin(lon), -np.sin(lat)]])
