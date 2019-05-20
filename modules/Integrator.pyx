import numpy as np

def IntegrateRK4(current_state, dt, func):
  return cIntegrateRK4(current_state, dt, func)

cdef cIntegrateRK4(current_state, dt, func):
  cdef t = current_state.time
  cdef x = current_state.position
  cdef v = current_state.velocity

  cdef float k1 = dt*func(x, v)
  cdef float k2 = dt*func(x + 0.5*dt, v + 0.5*k1)
  cdef float k3 = dt*func(x + 0.5*dt, v + 0.5*k2)
  cdef float k4 = dt*func(x + dt, v + k3)

  v = v + (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
  current_state.time = t + dt
  current_state.velocity = v
  return current_state
