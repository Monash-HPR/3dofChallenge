# Newtonian Gravitation

cdef class Gravity:

  cpdef void initialise(self, dict grav_props):
    self.mu = 3.9857e14

  # cdef double getGravitationalAcceleration(self):
  #   pass
