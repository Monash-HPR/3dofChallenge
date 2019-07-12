import logging
cimport numpy as np
import numpy as np

logger = logging.getLogger(__name__)

# Average angular velocity of Earth in rad/s
cdef double EARTH_OMEGA = 7.2921159e-5

# Transformation matrix of Earth w.r.t. inertial by time
cpdef np.ndarray T_EI_time(time):
    cdef double hour_angle = time * EARTH_OMEGA
    return T_EI(hour_angle)

# Transformation matrix of Earth w.r.t. inertial
cpdef np.ndarray T_EI(double xi):
    """
    Return a transformation matrix of Earth w.r.t inertial

    :param xi: hour angle
    :type xi: double

    """
    return np.array([
        [ np.cos(xi), np.sin(xi), 0],
        [-np.sin(xi), np.cos(xi), 0],
        [          0,          0, 1]
    ])

# Transformation matrix of inertial w.r.t. Earth by time
cpdef np.ndarray T_IE_time(time):
    cdef double hour_angle = time * EARTH_OMEGA
    return T_IE(hour_angle)

# Transformation matrix of inertial w.r.t. Earth
cpdef np.ndarray T_IE(double xi):
    return T_EI(xi).T

# Transformation matrix of geocentric w.r.t Earth
cpdef np.ndarray T_GE(double lat, double lon):
    return np.array([
        [-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon),  np.cos(lat)],
        [              -np.sin(lon),                np.cos(lon),            0],
        [-np.cos(lat) * np.cos(lon), -np.cos(lat) * np.sin(lon), -np.sin(lat)]
    ])

# Transformation matrix of Earth w.r.t geocentric
cpdef np.ndarray T_EG(double lat, double lon):
    return T_GE(lat, lon).T

# Transformation matrix of body w.r.t geocentric
cpdef np.ndarray T_BG(double yaw, double pitch, double roll):
    return np.array([
        [
            np.cos(yaw) * np.cos(pitch),
            np.sin(yaw) * np.cos(pitch),
            -np.sin(pitch)
        ],
        [
            np.cos(yaw) * np.sin(pitch) * np.sin(roll) - np.sin(yaw) * np.cos(roll),
            np.sin(yaw) * np.sin(pitch) * np.sin(roll) + np.cos(yaw) * np.cos(roll),
            np.cos(pitch) * np.sin(roll)
        ],
        [
            np.cos(yaw) * np.sin(pitch) * np.cos(roll) + np.sin(yaw) * np.sin(roll),
            np.sin(yaw) * np.sin(pitch) * np.cos(roll) - np.cos(yaw) * np.sin(roll),
            np.cos(pitch) * np.cos(roll)
        ]
    ])


# Transformation matrix of geocentric w.r.t. body
cpdef np.ndarray T_GB(double yaw, double pitch, double roll):
    return T_BG(yaw, pitch, roll).T

# Transformation matrix of inertial w.r.t. geocentric
cpdef np.ndarray T_IG(double time, double lat, double lon):
    return T_IE_time(time) @ T_EG(lat, lon)

# Transformation matrix of geocentric w.r.t. inertial
cpdef np.ndarray T_GI(double time, double lat, double lon):
    return T_GE(lat, lon) @ T_EI_time(time)