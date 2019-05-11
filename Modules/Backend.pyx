from Modules.Forces import Gravitation, Propulsion, Aerodynamics
from Modules.Forces cimport Gravitation, Propulsion, Aerodynamics

# instantiate the parts of the sim
cdef Propulsion.Motor propulsion = Propulsion.Motor()
cdef Gravitation.Gravity gravitation = Gravitation.Gravity()
cdef Aerodynamics.Aero aerodynamics = Aerodynamics.Aero()


cpdef void initialise(dict init_dict):
  # WILL DEAL WITH ALL INITIALISATION ERROR CHECKING HERE TO KEEP CODE IN OTHER
  # SECTIONS CLEAN AND UNDERSTANDABLE.
  # local error checking will be reserved for checking if things have gone wrong
  # during the course of a sim.


  # NOTE: CAN ALSO PROBABLY NOW MAKE ALL THE INIT FUNCTIONS C FUNCTIONS
  # and just access this one function through Python to initialise them all,
  # hopefully reducing the total overhead
  propulsion.initialise(init_dict['Propulsion'])
  aerodynamics.initialise(init_dict['Aerodynamics'])
  gravitation.initialise(init_dict['Gravitation'])
