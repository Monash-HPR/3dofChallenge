cimport libc.math as cmath

"""
What follows is the International Standard Atmosphere (ISA) values.
All results in SI units unless otherwise stated.
"""

# Constants
cdef double r0 = 6356766.0
cdef double R = 287.16
cdef double gamma = 1.4
cdef double dens0 = 1.225
cdef double p0 = 101325
cdef double g0 = 9.805
cdef double T0 = 298.15
cdef double lapse_rate = -0.0065

def geopotential(double h_gm):
  """
  Returns the geopotential (different from geometric) height.
  Arguments:
  double h_gm: The geometric height (m)
  Result:
  double altitude: The geopotential altitude, which will simply be the altitude
                   for the rest of this module.
  """
  return c_geopotential(h_gm)

cdef double c_geopotential(double h_gm):
  cdef double altitude = ((h_gm)/(1+(h_gm/r0)))
  return altitude

def temp(double altitude):
  """
  Returns the temperature.
  Arguments:
  double altitude: The geometric altitude (m)
  Result:
  double T: The temperature
  """
  return c_temp(altitude)

cdef double c_temp(double altitude):
  altitude = geopotential(altitude)
  cdef double T = T0 + lapse_rate*altitude
  return T

def pressure(double altitude):
  """
  Returns the pressure.
  Arguments:
  double altitude: The geometric altitude (m)
  Result:
  double P: The pressure (Pa)
  """
  return c_pressure(altitude)

cdef double c_pressure(double altitude):
  altitude = geopotential(altitude)
  cdef double p = p0*cmath.pow((temp(altitude)/T0), (-g0/(lapse_rate*R)))
  return p

def density(double altitude):
  """
  Returns the temperature.
  Arguments:
  double altitude: The geometric altitude (m)
  Result:
  double rho: The density (kg/m^3)
  """
  return c_density(altitude)

cdef double c_density(double altitude):
  altitude = geopotential(altitude)
  cdef double rho = pressure(altitude)/(R*temp(altitude))
  return rho

def speedsound(double altitude):
  return c_speedsound(altitude)

cdef double c_speedsound(double altitude):
  T = temp(altitude)
  cdef double a = cmath.sqrt(gamma*R*T)
  return a
