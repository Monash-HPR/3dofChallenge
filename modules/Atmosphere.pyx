cimport libc.math as cmath

# constants
cdef double r0 = 6356766.0
cdef double R = 287.16
cdef double gamma = 1.4
cdef double dens0 = 1.225
cdef double p0 = 101325
cdef double g0 = 9.805
cdef double T0 = 298.15
cdef double lapse_rate = -0.0065

def geopotential(double h_gm):
  return c_geopotential(h_gm)

cdef double c_geopotential(double h_gm):
  cdef double altitude = ((h_gm)/(1+(h_gm/r0)))
  return altitude

def temp(double altitude):
  return c_temp(altitude)

cdef double c_temp(double altitude):
  cdef double T = T0 + lapse_rate*altitude
  return T

def pressure(double altitude):
  return c_pressure(altitude)

cdef double c_pressure(double altitude):
  cdef double p = p0*cmath.pow((temp(altitude)/T0), (-g0/(lapse_rate*R)))
  return p

def density(double altitude):
  return c_density(altitude)

cdef double c_density(double altitude):
  cdef double rho = pressure(altitude)/(R*temp(altitude))
  return rho
