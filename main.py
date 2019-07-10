from Modules import Structures
from Modules.Forces import Inertia
from Modules import Integrator
import matplotlib.pyplot as plt
import numpy as np
import copy

# Dictionary below that contains the initial conditions required for simulation
initial_conditions = {
    "time": 0.0,                # Time to start simulation (s)
    "dt_initial": 0.1,          # Initial time step size
    "mass_dry": 25,             # Mass of the rocket without propellant
    "mass_propellant": 9,       # Mass of propellant
    "latitude": -37.8136,       # Range latitude    (degrees)
    "longitude": 144.9631,      # Range longitude   (degrees)
    "altitude": 0,              # Range altitude    (m)
    "burn_time": 3.5,           # motor burn Time   (s)
    "thrust": 5800,             # motor burn thrust   (N)
    "reference_area": 0.013893  # reference area (tube cross-section) (m^2)
    }



# Initialise the state class with initial conditions
State = Structures.initialiseState(initial_conditions)
altitude = [Structures.getAltitude(State)]
time = [State.time]
velocity = [np.linalg.norm(State.vB_E_D)]
acceleration = [np.linalg.norm(Structures.get_aB_I_I(State))]


# Main Loop
while (State.time < 300):
    Integrator.eulerIntegration(State)




    altitude.append(Structures.getAltitude(State))
    time.append(State.time)
    velocity.append(np.linalg.norm(State.vB_E_D))
    acceleration.append(np.linalg.norm(State.aB_I_I))



# Post - Processing



# Plotting
plt.subplot(131)
plt.plot(time, altitude)
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.subplot(132)
plt.plot(time, velocity)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.subplot(133)
plt.plot(time, acceleration)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')

plt.show()
