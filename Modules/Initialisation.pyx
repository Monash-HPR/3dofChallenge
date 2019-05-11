import Propulsion


def initialise(dict init_dict):
  # WILL DEAL WITH ALL INITIALISATION ERROR CHECKING HERE TO KEEP CODE IN OTHER
  # SECTIONS CLEAN AND UNDERSTANDABLE.
  # local error checking will be reserved for checking if things have gone wrong
  # during the course of a sim.
  Propulsion.initialise(init_dict['Propulsion'])
