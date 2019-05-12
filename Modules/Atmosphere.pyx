import logging
import numpy as np

cdef double GAS_CONSTANT = 286.0
cdef double SPEC_HEAT_RATIO = 1.4
cdef double LAPSE_RATE = 0.00649 # NOTE: Only valid to 11000m (36k ft)
cdef double KELVIN_OFFSET = 273.15
cdef double ATMOSPHERIC_TEMP_OFFSET = 15.04

logger = logging.getLogger(__name__)

cpdef double mach_to_ms(double vel, double alt):
    return vel*get_speed_of_sound(alt)

cpdef double ms_to_mach(double vel, double alt):
    return vel/get_speed_of_sound(alt)

cpdef double get_density(double alt):
    cdef double temp = get_atmospheric_temp(alt)
    return 101.29 * np.power((temp)/288.08, 5.256)

cpdef double get_speed_of_sound(double alt):
    cdef double temp = get_atmospheric_temp(alt)
    return np.sqrt(SPEC_HEAT_RATIO * GAS_CONSTANT * temp)

cpdef double kelvin_to_celsius(double temp):
    return temp - KELVIN_OFFSET

cpdef double celsius_to_kelvin(double temp):
    return temp + KELVIN_OFFSET

cpdef double get_atmospheric_temp(double alt):
    cdef double temp_celsius = ATMOSPHERIC_TEMP_OFFSET - LAPSE_RATE * alt
    return celsius_to_kelvin(temp_celsius)

logger.debug('Atmosphere Module Loaded')