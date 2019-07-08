import numpy as np
from Modules import Geodesy


def skewSymmetricExpansion(vector):
    # Takes a vector and returns the Skew-Symmetric matrix expansion
    x1 = vector[0]
    x2 = vector[1]
    x3 = vector[2]
    return np.array([ [0.0, -x3, x2], [x3, 0.0, -x1], [-x2, x1, 0]])

def get_T_DI(sBI__I):
    # Create the transformation matrix from geodetic coordinates to inertial coordinates
    geodetic_postion = Geodesy.getGeodeticPosition(sBI__I)
    lat = geodetic_postion[0]           # Geodetic latitude
    lon = geodetic_position[1]          # Celestial longitude

    return np.array([   [-np.sin(lat) * cos(lon), -np.sin(lat) * sin(lon), np.cos(lon)],
                        [-np.sin(lon), np.cos(lon), 0.0],
                        [-np.cos(lat) * np.cos(lon), -np.cos(lon) * np.sin(lon), -np.sin(lat)]])

def get_T_DG(sBI__I):
    delta = getDeflectionAngle(sBI__I) # This wont be the correct delta, Needs addressing
    return np.array([   [np.cos(delta), 0.0, np.sin(delta)]
                        [0, 1, 0]
                        [-np.sin(delta), 0, np.cos(delta)]])
