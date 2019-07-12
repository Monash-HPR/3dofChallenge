import logging
cimport numpy as np
import numpy as np

logger = logging.getLogger(__name__)

# Necessary environmental constants
cdef double GAS_CONSTANT = 286.0
cdef double SPEC_HEAT_RATIO = 1.4
cdef double LAPSE_RATE = 0.00649
cdef double KELVIN_OFFSET = 273.15
cdef double ATMOSPHERIC_TEMP_OFFSET = 288.15

cpdef np.ndarray mach_to_ms(np.ndarray vel, double alt):
    """
    Convert velocity from m/s to mach given a specific altitude.

    :param vel: Vector of velocity components in m/s
    :type vel: np.ndarray
    :returns: Velocity in mach
    """
    return np.multiply(vel, get_speed_of_sound(alt))

cpdef np.ndarray ms_to_mach(np.ndarray vel, double alt):
    """
    Convert velocity from mach to m/s given a specific altitude.

    :param vel: Vector of velocity components in mach
    :type vel: np.ndarray
    :returns: Velocity in m/s
    """
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
    """
    Calculate the atmospheric air density at a specific altitude.

    :param alt: Altitude in metres
    :type alt: double
    :returns: Density in kg/m^3

    """
    cdef double pressure = get_pressure(alt)
    cdef double temp = get_atmospheric_temp(alt)
    return pressure/(GAS_CONSTANT * temp)

cpdef double get_speed_of_sound(double alt):
    """
    Calculate the speed of sound at a specific altitude

    :param alt: Altitude in metres
    :type alt: double
    :returns: Sonic speed in m/s

    """

    cdef double temp = get_atmospheric_temp(alt)
    return np.sqrt(SPEC_HEAT_RATIO * GAS_CONSTANT * temp)

cpdef double kelvin_to_celsius(double temp):
    """
    Convert temperature from Kelvin to Celsius

    :param temp: Temperature in Kelvin
    :type temp: double
    :returns: Temperature in Celsius
    """
    return temp - KELVIN_OFFSET

cpdef double celsius_to_kelvin(double temp):
    """
    Convert temperature from Celsius to elvin

    :param temp: Temperature in Celsius
    :type temp: double
    :returns: Temperature in Kelvin
    """
    return temp + KELVIN_OFFSET

cpdef double get_atmospheric_temp(double alt):
    """
    Get standard atmospheric temperature at a specific altitude

    :param alt: Altitude in metres
    :type alt: double
    :returns: Temperature in Kelvin
    """
    cdef double temp_kelvin = ATMOSPHERIC_TEMP_OFFSET - LAPSE_RATE * alt
    return temp_kelvin

logger.debug('Atmosphere Module Loaded')