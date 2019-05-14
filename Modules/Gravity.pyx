import logging
cimport numpy as np
import numpy as np

cdef double G = 6.67408e-11
cdef double MASS_EARTH = 5.9722e24
cdef double RADIUS_EARTH = 6371000.0

logger = logging.getLogger(__name__)

cdef class Gravity:
    def __init__(self):
        return
    
    cpdef get_force(self, double alt, double mass):
        return G*MASS_EARTH*mass/np.power(RADIUS_EARTH+alt, 2)
