from Modules import Structures
from Modules import Geodesy
import time

# Dictionary below that contains the initial conditions required for simulation
initial_conditions = {
    "time": 0.0,            # Time to start simulation (s)
    "dt_initial": 0.1,      # Initial time step size
    "mass_dry": 25,         # Mass of the rocket without propellant
    "mass_propellant": 9,   # Mass of propellant
    "latitude": -37.8136,   # Range latitude    (degrees)
    "longitude": 144.9631,  # Range longitude   (degrees)
    "altitude": 0,        # Range altitude    (m)
    "burn_time": 3.5,       # motor burn Time   (s)
    "thrust": 5800          # motor burn Time   (N)
    }



# Initialise the state class with initial conditions
State = Structures.initialiseState(initial_conditions)
g = Geodesy.get_g__G(State)
print(g)
