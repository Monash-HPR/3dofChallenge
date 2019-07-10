import numpy as np

# Define global constants:
# Constants sourced from WGS84.
a = 6378137.0                    # Semi-major axis of the Earth (m)
f = 1/298.257223563              # Flattening parameter of the Earth
b = a * (1 - f)                  # Polar axis (semi-minor axis)
GM = 3986004.418e8               # Earth's gravitational constant (m**3/s**2)
omega_earth = 7292115e-11        # Angular velocity of the Earth
C20 = -4.841688e-4               # Second-degree zonal gravitational coefficent


def get_g__G(State):
    # Calculates the gravitational vector in geographic coordinates using a spheroidal, rotating Earth model of the state vector
    sBI_norm = np.linalg.norm(State.sBI__I)
    geocentric_lat = np.asscalar(getGeocentricLatitude(State.sBI__I))
    return GM / sBI_norm**2 * np.array([   [-3 * np.sqrt(5) * C20 * (a / sBI_norm)**2 * np.sin(geocentric_lat) * np.cos(geocentric_lat)], [0.0], [1 + 1.5 * C20 * (a / sBI_norm)**2 * (3 * np.sin(geocentric_lat) - 1)]])

def getGeocentricLatitude(sBI__I):
    # Retrieves the geocentric latitude of the state vector
    sBI_norm = np.linalg.norm(sBI__I)
    return np.arcsin(sBI__I[2]/sBI_norm)

def getApproximateDeflectionAngle(geodetic_lat, h):
    # Calculates the angle between the geocentric latitude and the geodetic latitude
    R0 = getR0(geodetic_lat)
    return f * np.sin(2 * geodetic_lat) * (1 - f/2 - h/R0)

def getDeflectionAngle(sBI__I, time):
    geodetic_pos = getGeodeticPosition(sBI__I, time)
    geodetic_lat = geodetic_pos[0]
    geocentric_lat = getGeocentricLatitude(sBI__I)
    return geodetic_lat - geocentric_lat

def getGeodeticPosition(sBI__I, time):
    # Retrives the geodetic position from the state vector.
    # As the geodetic latitude and longitude are unkown. this must be acquire through an iterative process

    # Set geodetic latitude to gecentric latitude to begin routine
    geocentric_lat = getGeocentricLatitude(sBI__I)
    geodetic_lat = geocentric_lat
    geodetic_lat_last = geodetic_lat + 1
    sBI_norm = np.linalg.norm(sBI__I)
    iter = 0

    # Perform iterations to calculate geodetic latitude
    while (np.abs(geodetic_lat_last - geodetic_lat) > 1e-6) and (iter < 15):
        geodetic_lat_last = geodetic_lat
        R0 = getR0(geodetic_lat)
        h = sBI_norm - R0
        delta = getApproximateDeflectionAngle(geodetic_lat, h)
        geodetic_lat = delta + geocentric_lat
        iter += 1

    # Now calculate celestial longitude as a correction is required due to the rotation of the Earth
    # NOTE: There should be an initial greenwich meridian longitude term that idk how to deal with rn.
    geodetic_lon = np.arcsin(sBI__I[1]/np.sqrt(sBI__I[0]**2 + sBI__I[1]**2)) - omega_earth*time

    return np.array([[geodetic_lat], [geodetic_lon], [h]])

def getR0(geodetic_lat):
    # Returns the value R0 which is used in calculating the
    return a * (1 - 0.5 * f * (1 - np.cos(2 * geodetic_lat)) + 5 * f**2 / 16 * (1 - np.cos(4 * geodetic_lat)))

def get_WBE__I():
    # Function retrievs the angular velocity vector of the Earth in Inertial coordinates
    return np.array([ [0.0], [0.0], [omega_earth]])

def getGeocentricPosition(geodetic_position):
    # Converts spherical geodetic coordinates (spheroidal Earth) to cartesian geocentric (Earth) coordinates
    geodetic_lat = geodetic_position[0,0]
    lon = geodetic_position[1,0]
    geodetic_alt = geodetic_position[2,0]
    sin_lat = np.sin(geodetic_lat)
    cos_lat = np.cos(geodetic_lat)
    sin_lon = np.sin(lon)
    cos_lon = np.cos(lon)
    N = a**2 / np.sqrt( ( a * cos_lat)**2 + (b * sin_lat)**2)
    return np.array( [[(N + geodetic_alt) * cos_lat * cos_lon], [(N + geodetic_alt) * cos_lat * sin_lon], [(N * (b/a)**2 + geodetic_alt) * sin_lat]])
