# Main sim loop and associated setup/initialisation
from Modules.Backend import *
from Modules import Structures

init_settings = {
  'State': {
                  'frame_mass': 24.0
  },
  'Integrator': {
                  'dt': 0.1,
                  'method': 'rk4'
  },
  'Gravitation': {},
  'Propulsion': {
                  'time_burnout': 9.0, # s
                  'mass_propellant_initial': 4.249, # kg
                  'mass_total_initial': 6.9854, # kg
                  'thrust_avg': 837.9, # N
  },
  'Aerodynamics': {}
  }

# initialisation
state = Structures.State()
initialise(init_settings)
# print(propulsion.getPropellantMass(0.0))

# print(Propulsion.getPropellantMass(0.0))
f = lambda x: 0 # RHS function
print(state.a)

print(state.a)
