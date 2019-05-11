# Main sim loop and associated setup/initialisation
from Modules import Structures, Transformations, Integrator, Initialisation
from Modules.Forces import Gravitation, Propulsion, Aerodynamics

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
s = Structures.State()

Initialisation.initialise(init_settings)
# Propulsion.initialise(init_settings['Propulsion'])

print(Propulsion.getPropellantMass(0.0))
f = lambda x: 0 # RHS function
print(s.a)
# s = Integrator.integrate_Rk4(f, s, 0.01)
print(s.a)
