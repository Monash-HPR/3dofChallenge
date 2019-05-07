# Definitions for 'State' and other classes
# Maybe include a testing class here?

cdef class State:
  
  def __init__(self):
   self._a = 0

  @property
  def a(self):
    return self._a

  @a.setter
  def a(self, val):
    self._a = val
