import numpy as np
from Modules import Transformations

# Define global constants:
# Constants sourced from WGS84.
a = 6378137.0                    # Semi-major axis of the Earth (m)
f = 1/298.257223563              # Flattening parameter of the Earth
b = a * (1 - f)                  # Polar axis (semi-minor axis)
GM = 3986004.418e8               # Earth's gravitational constant (m**3/s**2)
omega_earth = 7292115e-11        # Angular velocity of the Earth
C20 = -4.841688e-4               # Second-degree zonal gravitational coefficent

def getGeocentricPosition(State):
    # Converts spherical geodetic coordinates (spheroidal Earth) to cartesian geocentric (Earth) coordinates
    sBI_norm = np.linalg.norm(State.sBI__I)
    State.lat = np.asscalar(np.arcsin(State.sBI__I[2]/sBI_norm))
    State.lon = np.asscalar(np.arcsin(State.sBI__I[1]/np.sqrt(State.sBI__I[0]**2 + State.sBI__I[1]**2)))
    alt = sBI_norm - a
    sin_lat = np.sin(State.lat)
    cos_lat = np.cos(State.lon)
    sin_lon = np.sin(State.lon)
    cos_lon = np.cos(State.lon)
    r = (alt + a)
    x = r * cos_lon
    y = r * sin_lon
    z = r * sin_lat
    return np.array( [[x], [y], [z]])
