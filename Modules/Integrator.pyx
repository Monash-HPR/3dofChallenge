#3DoF integrator
cimport Structures

cdef c_integrate_Rk4( state):
  state.a = 2
  return state

def integrate_Rk4(state not None):
  return c_integrate_Rk4(state)
