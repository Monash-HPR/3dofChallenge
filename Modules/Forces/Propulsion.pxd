cdef class Motor:
  cdef:
    double thrust_avg, time_burnout
    double mass_propellant_initial, mass_total_initial, mass_casing
    bint is_initialised

  cpdef void initialise(self, dict motor_props)

  cpdef double getTotalMass(self, double time)

  cpdef double getPropellantMass(self, double time)

  cpdef double thrust(self, double time)
