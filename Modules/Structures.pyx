# Definitions for 'State' and other classes
# Maybe include a testing class here?

cdef class State(object):
  cdef:
    double _a

  def __cinit__(self):
    self._a = 1

  @property
  def a(self):
    return self._a

  @a.setter
  def a(self, val):
    self._a = val
