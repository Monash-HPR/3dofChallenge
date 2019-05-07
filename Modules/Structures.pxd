cdef class State:
  cdef:
    double _a, a
    double sBI__I[3], vB_I_I[3], aB_I_I[3]
