import numpy as np

# Define global constants:
# Constants sourced from WGS84.
a = 6378137.0                    # Semi-major axis of the Earth (m)
f = 1/298.257223563              # Flattening parameter of the Earth
GM = 3986004.418e8            # Earth's gravitational constant (m**3/s**2)
omega_earth = 7292115e-11     # Angular velocity of the Earth
C20 = -4.841688e-4            # Second-degree zonal gravitational coefficent


def get_g__G(State):
    # Calculates the gravitational vector in geographic coordinates using a spheroidal, rotating Earth model of the state vector
    sBI_norm = np.linalg.norm(State.sBI__I)
    geocentric_lat = getGeocentricLatitude(State)
    return GM / sBI_norm**2 * np.array([   [-3 * np.sqrt(5) * C20 * (a / sBI_norm)**2 * np.sin(geocentric_lat) * np.cos(geocentric_lat)], [0.0], [1 + 1.5 * C20 * (a / sBI_norm)**2 * (3 * np.sin(geocentric_lat) - 1)]])

def getGeocentricLatitude(State):
    # Retrieves the geocentric latitude of the state vector
    sBI_norm = np.linalg.norm(State.sBI__I)
    return np.arcsin(State.sBI__I[2]/sBI_norm)

def getApproximateDeflectionAngle(altitude):
    # Calculates the angle between the geocentric latitude and the geodetic latitude
    geodetic_lat = getGeodeticLatitude(State)
    R0 = getR0()
    return f * np.sin(2 * geodetic_lat) * (1 - f/2 - altitude/R0)

def getDeflectionAngle(State):
    geodetic_pos = getGeodeticPosition(State)
    geodetic_lat = geodetic_pos[0]
    geocentric_lat = getGeocentricLatitude(State)
    return geodetic_lat - geocentric_lat

def getGeodeticPosition(State):
    # Retrives the geodetic position from the state vector.
    # As the geodetic latitude and longitude are unkown. this must be acquire through an iterative process

    # Set geodetic latitude to gecentric latitude to begin routine
    geocentric_lat = getGeocentricLatitude(State)
    geodetic_lat = geocentric_lat
    geodetic_lat_last = geodetic_lat + 1
    sBI_norm = np.linalg.norm(State.sBI__I)
    iter = 0

    # Perform iterations to calculate geodetic latitude
    while (np.abs(geodetic_lat_last - geodetic_lat) > 1e-6) and (iter < 15):
        geodetic_lat_last = geodetic_lat
        r = getR0(geodetic_lat)
        h = sBI_norm - R0
        delta = getApproximateDeflectionAngle(h)
        geodetic_lat = delta + geocentric_lat
        iter += 1

    # Now calculate geodetic longitude as a correction is required due to the rotation of the Earth
    geodetic_lon = arcsin(state.sBI_I_I[2]/np.sqrt(state.sBI_I_I[1]**2 + state.sBI_I_I[1]**2)) - lGO - omega_earth(State.time)

    return np.array([[geodetic_lat], [geodetic_lon], [sBI_norm]])

def getR0(geodetic_lat):
    # Returns the value R0 which is used in calculating the
    return a * (1 - 0.5 * f * (1 - np.cos(2 * geodetic_lat)) + 5 * f**2 / 16 * (1 - np.cos(4 * geodetic_lat)))
