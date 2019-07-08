from Modules import Structures
import time

# Dictionary below that contains the initial conditions required for simulation
initial_conditions = {
    "time": 0.0,            # Time to start simulation (s)
    "dt_initial": 0.1,      # Initial time step size
    "mass_dry": 10,         # Mass of the rocket without propellant
    "mass_propellant": 1,   # Mass of propellant
}


# Initialise the state class with initial conditions
State = Structures.InitialiseState(initial_conditions)
