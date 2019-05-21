cimport libc.math as cmath
import numpy as np
cimport numpy as np

# If you add any more cdef functions in here, those MUST be declared in the equivalent PXD file.

def T_EI (double time):
  """
  Returns the transformation matrix to go from earth (or geocentric) to inertial.
  Arguments:
  double time: the time of the state.
  Result:
  T_EI: a 3x3 np.ndarray transformation matrix.
  """
  return c_T_EI(time)

cdef np.ndarray c_T_EI (double time):
  cdef omega_EI = 7.292115*cmath.pow(10, -5) #rad/s
  cdef h_ang = omega_EI*time
  return np.array ([[cmath.cos(h_ang), cmath.sin(h_ang), 0],
  [-cmath.sin(h_ang), cmath.cos(h_ang), 0],
  [0,0,1]])

def T_GE (np.ndarray pos_g):
  return c_T_GE(pos_g)

cdef np.ndarray c_T_GE (np.ndarray pos_g):
  """
  Returns the transformation matrix to go from geographic to Earth (or geocentric).
  Variables:
  double lat: the latitude
  double long: the longitude
  Result:
  T_EI: a 3x3 np.ndarray transformation matrix.
  """
  cdef double lat = pos_g[0]
  cdef double lon = pos_g[1]
  return np.array ([[-cmath.sin(lat)*cmath.cos(lon), -cmath.sin(lat)*cmath.sin(lon), cmath.cos(lat)],
  [-cmath.sin(lon), cmath.cos(lon), 0],
  [-cmath.cos(lat)*cmath.cos(lon),-cmath.cos(lat)*cmath.sin(lon),-cmath.sin(lat)]])

def T_VG (np.ndarray vel_g):
  return c_T_VG(vel_g)

cdef np.ndarray c_T_VG (np.ndarray vel_g):
  """
  Returns the transformation matrix to go from 'velocity coordinates' to geographic (lat. and long.)
  Arguments:
  np.ndarray vel_g: A 3x1 list of the velocities in GEOGRAPHIC coordinates, corresponding to [N, E, centre].
  Variables:
  double gamma: The heading angle
  double chi: The flight path angle
  Result:
  T_VG: a 3x3 np.ndarray transformation matrix.
  """
  cdef double gamma, chi
  if vel_g[0] == 0:
    if vel_g[1] == 0:
      gamma = 0
      chi = 0
    else:
      chi = np.pi/2
      gamma = cmath.atan(vel_g[1]/vel_g[0])
  else:
    gamma = cmath.atan(vel_g[1]/vel_g[0])
    chi = cmath.atan(-vel_g[2]/(cmath.sqrt( cmath.pow(vel_g[0], 2) + cmath.pow(vel_g[1], 2) )) )

  return np.array ([[cmath.cos(gamma)*cmath.cos(chi), cmath.cos(gamma)*cmath.sin(chi), -cmath.sin(gamma)],
  [-cmath.sin(chi), cmath.cos(chi), 0],
  [cmath.sin(gamma)*cmath.cos(chi), cmath.sin(gamma)*cmath.sin(chi),cmath.cos(gamma)]])

def T_GI (np.ndarray pos_g, double time):
  result = np.matmul(T_GE(pos_g), T_EI(time))
  return result
