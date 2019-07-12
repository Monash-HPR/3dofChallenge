import logging
cimport numpy as np
import numpy as np

cdef double GM = 3.986005e14
cdef double RADIUS_EARTH = 6371000.0

logger = logging.getLogger(__name__)

cdef class Gravity:
    def __init__(self):
        logger.debug('Creating Gravity Instance')
        return
    
    cpdef get_aB_E_G(self, np.ndarray sBE__G):
        cdef double alt = sBE__G[1]
        return np.array([0.0, -GM/np.power(RADIUS_EARTH+alt, 2), 0.0], np.float64)

logger.debug('Gravity Module Loaded')
