import numpy as np
from Modules import Geodesy


def skewSymmetricExpansion(vector):
    # Takes a vector and returns the Skew-Symmetric matrix expansion
    x1 = vector[0]
    x2 = vector[1]
    x3 = vector[2]
    return np.array([ [0.0, -x3, x2], [x3, 0.0, -x1], [-x2, x1, 0]])

def get_T_DG(State):
    getGeodeticPosition(State)

def initial_T_DG(sBI__G): #unsure if this is needed
    geocentric_lat = Geosdesy.getGeocentricLatitude(State)
    geodetic_lat = geocentric_lat
    geodetic_lat_last = geodetic_lat + 1
    sBI_norm = np.linalg.norm(State.sBI__I)
    iter = 0

    # Perform iterations to calculate geodetic latitude
    while (np.abs(geodetic_lat_last - geodetic_lat) > 1e-6) and (iter < 15):
        geodetic_lat_last = geodetic_lat
        r = getR0(geodetic_lat)
        h = sBI_norm - R0
        delta = Geodesy.getApproximateDeflectionAngle(h)
        geodetic_lat = delta + geocentric_lat
        iter += 1

    # Now calculate geodetic longitude as a correction is required due to the rotation of the Earth
    geodetic_lon = arcsin(state.sBI_I_I[2]/np.sqrt(state.sBI_I_I[1]**2 + state.sBI_I_I[1]**2)) - lGO - omega_earth(State.time)
    return

def get_T_DI(State):
    # Create the transformation matrix from geodetic coordinates to inertial coordinates
    geodetic_postion = Geodesy.getGeodeticPosition(State.sBI__I)
    lat = geodetic_postion[0]           # Geodetic latitude
    lon = geodetic_position[1]          # Celestial longitude

    return np.array([   [-np.sin(lat) * cos(lon), -np.sin(lat) * sin(lon), np.cos(lon)],
                        [-np.sin(lon), np.cos(lon), 0.0],
                        [-np.cos(lat) * np.cos(lon), -np.cos(lon) * np.sin(lon), -np.sin(lat)]])
