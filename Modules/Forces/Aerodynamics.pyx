# Aerodynamics

# Plan:
# FUCK KNOWS

# More readable import code
# -Better calculation/use of centre of pressure
# -More justified/improved use of multidimensional interpolation i.e. dealing with vector y = f(vector x)
# -Reduced interdependency between functions
# -Overall speed increase

cdef class Aero:

  cpdef void initialise(self, dict aero_props):
    cdef double a = 1
