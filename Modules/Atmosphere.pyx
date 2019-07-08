import logging
cimport numpy as np
import numpy as np

cdef double GAS_CONSTANT = 286.0
cdef double SPEC_HEAT_RATIO = 1.4
cdef double LAPSE_RATE = 0.00649
cdef double KELVIN_OFFSET = 273.15
cdef double ATMOSPHERIC_TEMP_OFFSET = 288.15

logger = logging.getLogger(__name__)

cpdef np.ndarray mach_to_ms(np.ndarray vel, double alt):
    return np.multiply(vel, get_speed_of_sound(alt))

cpdef np.ndarray ms_to_mach(np.ndarray vel, double alt):
    return np.divide(vel, get_speed_of_sound(alt))

cpdef double get_pressure(double alt):
    """
    Get the atmospheric pressure in Pascals.
    Assumes tropospheric altitudes (<11km)

    :param alt: Altitude in metres
    :type alt: double
    :returns: Density in Pascals

    """
    cdef double temp = get_atmospheric_temp(alt)
    return 101325 * np.power(temp/288.15, 5.2559)

cpdef double get_density(double alt):
    cdef double pressure = get_pressure(alt)
    cdef double temp = get_atmospheric_temp(alt)
    return pressure/(GAS_CONSTANT * temp)

cpdef double get_speed_of_sound(double alt):
    cdef double temp = get_atmospheric_temp(alt)
    return np.sqrt(SPEC_HEAT_RATIO * GAS_CONSTANT * temp)

cpdef double kelvin_to_celsius(double temp):
    return temp - KELVIN_OFFSET

cpdef double celsius_to_kelvin(double temp):
    return temp + KELVIN_OFFSET

cpdef double get_atmospheric_temp(double alt):
    cdef double temp_kelvin = ATMOSPHERIC_TEMP_OFFSET - LAPSE_RATE * alt
    return temp_kelvin

logger.debug('Atmosphere Module Loaded')