cdef class Gravity:

  cdef:
    double mu

  cpdef void initialise(self, dict grav_props)
