#3DoF integrator
from Structures cimport State


cdef State c_integrate_Rk4(state, double dt):
  """
  Function to compute the 4th order Runge-Kutta method integration step on the
  State class' velocity and position vectors.
  All calculations are performed in the inertial reference frame and inertial
  coordinate system.

  Inputs:
    -A State class instance, the state of the simulation at time t0.
    -A float dt, the timestep for the integration.
  Outputs:
    -A State class instance, the propagated state of the simulation at time
      t0 + dt.


  General Scheme (accuracy of O(dt^4)):
  For the ODE dy/dt = f(t, y(t)) with y(t0) = y0

  k1 = f(t0, y0)
  k2 = f(y0 + 1/2 * k1 * dt, t0 + 1/2 * dt)
  k3 = f(y0 + 1/2 * k2 * dt, t0 + 1/2 * dt)
  k4 = f(y0 + k3 * dt, t + dt)

  Result
  y(t0 + dt) = y0 + 1/6 * dt * (k1 + 2*k2 + 2*k3 + k4)
  """

  # state.a = 2 * dt
  return state


def integrate_Rk4(State state not None, double dt=0.01):
  return c_integrate_Rk4(state, dt)
