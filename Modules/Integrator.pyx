#3DoF integrator
from Structures import State
from copy import deepcopy
import numpy as np
cimport numpy as np

cdef c_integrate_Rk4(fn, state, double dt):
  """
  Function to compute the 4th order Runge-Kutta method integration step on the
  State class' velocity and position vectors.
  All calculations are performed in the inertial reference frame and inertial
  coordinate system.

  Inputs:
    -A RHS function fn, which takes the current state and returns the vector
      f(state) = d/dt([x1, x2, x3, v1, v2, v3])^T = [v1, v2, v3, a1, a2, a3]^T
    -A State class instance, the state of the simulation at time t0.
    -A float dt, the timestep for the integration.
  Outputs:
    -A State class instance, the propagated state of the simulation at time
      t0 + dt.


  General Scheme (O(dt^4) accurate):
  Based on the description given at:
  https://lpsa.swarthmore.edu/NumInt/NumIntFourth.html

  For the ODE dy/dt = f(t, y(t)) with y(t0) = y0

  y = [x1, x2, x3, v1, v2, v3]^T

  k1 = f(t0, y0)
  k2 = f(y0 + 1/2 * k1 * dt, t0 + 1/2 * dt)
  k3 = f(y0 + 1/2 * k2 * dt, t0 + 1/2 * dt)
  k4 = f(y0 + k3 * dt, t + dt)

  Result
  y_f = y0 + 1/6 * dt * (k1 + 2*k2 + 2*k3 + k4)
  """
  cdef double t

  # k vectors:
  cdef np.ndarray[double, ndim = 1] k1, k2, k3, k4  # update vectors

  k1 = fn(state)

  return state


def integrate_Rk4(RHS_function, state not None, double dt=0.01):
  return c_integrate_Rk4(RHS_function, state, dt)
