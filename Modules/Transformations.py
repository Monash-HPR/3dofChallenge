import numpy as np
from Modules import Geodesy

def skewSymmetricExpansion(vector):
    # Takes a vector and returns the Skew-Symmetric matrix expansion
    x1 = np.asscalar(vector[0])
    x2 = np.asscalar(vector[1])
    x3 = np.asscalar(vector[2])
    return np.array([ [0.0, -x3, x2], [x3, 0.0, -x1], [-x2, x1, 0]])

def get_T_DI(sBI__I, time):
    # Create the transformation matrix from geodetic coordinates to inertial coordinates
    geodetic_position = Geodesy.getGeodeticPosition(sBI__I, time)
    lat = np.asscalar(np.asscalar(geodetic_position[0]))     # Geodetic latitude
    lon = np.asscalar(np.asscalar(geodetic_position[1]))    # Geodetic longitude
    
    return np.array([   [-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lon)],
                        [-np.sin(lon), np.cos(lon), 0.0],
                        [-np.cos(lat) * np.cos(lon), -np.cos(lon) * np.sin(lon), -np.sin(lat)]])

def get_T_DG(sBI__I, time):
    delta = np.asscalar(np.asscalar(Geodesy.getDeflectionAngle(sBI__I, time))) # This wont be the correct delta, Needs addressing
    return np.array([   [np.cos(delta), 0.0, np.sin(delta)],
                        [0.0, 1.0, 0.0],
                        [-np.sin(delta), 0.0, np.cos(delta)]])

def get_T_GI(sBI__I,time):
    # This function returns the transformation matrix from inertial coordinates to geographic coordinates.
    # This transformation is time dependent as the celestial longitude and geodetic latitude depend on the rotation of the Earth.
    T_DI = get_T_DI(sBI__I,time)
    T_DG = get_T_DG(sBI__I,time)
    return np.matmul(np.transpose(T_DI),T_DG)

def get_T_EI(time):
    # This function returns the transformation matrix from geocentric coordinates to the inertial coordinate system
    wEI = Geodesy.omega_earth
    hour_angle = wEI * time
    return  np.array([[np.cos(hour_angle), np.sin(hour_angle), 0],
                    [-np.sin(hour_angle), np.cos(hour_angle), 0],
                    [0, 0, 1]])

def get_T_BG(euler_angles):
    # Returns the transformation between body coordinates and Earth coordinates.
    # NOTE: Needs an error check for gimbal locking
    theta = np.asscalar(euler_angles[0])
    psi = np.asscalar(euler_angles[1])
    phi = np.asscalar(euler_angles[2])
    return np.array([   [np.cos(phi) * np.cos(theta), np.sin(psi) * np.cos(theta), -np.sin(theta)],
                        [np.cos(psi) * np.sin(theta) * np.sin(phi) - np.sin(psi) * np.cos(phi), np.sin(psi) * np.sin(theta) * np.sin(phi) + np.cos(psi) * np.cos(phi), np.cos(theta) * np.cos(phi)],
                        [np.cos(psi) * np.sin(theta) * np.cos(phi) + np.sin(psi) * np.sin(phi), np.sin(psi) * np.sin(theta) * np.cos(phi) - np.cos(psi) * np.sin(phi), np.cos(theta) * np.cos(phi)]])

