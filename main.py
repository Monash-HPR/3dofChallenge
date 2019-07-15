from Modules import Structures
from Modules import Geodesy
from Modules import Integrator
import matplotlib.pyplot as plt
import numpy as np
import time

# Dictionary below that contains the initial conditions required for simulation
initial_conditions = {
    "time": 0.0,                # Time to start simulation (s)
    "dt_initial": 0.1,          # Initial time step size
    "mass_dry": 25,             # Mass of the rocket without propellant
    "mass_propellant": 9,       # Mass of propellant
    "latitude": 0,       # Range latitude    (degrees)
    "longitude": 0,      # Range longitude   (degrees)
    "altitude": 0,              # Range altitude    (m)
    "burn_time": 3.5,           # motor burn Time   (s)
    "thrust": 5800,             # motor burn Time   (N)
    "reference_area": 0.013893, # reference area (tube cross-section) (m^2)
    "parachute_Cd": 2,          # Parachute drag coefficient
    "parachute_area": 4.154,    # Parachute area (m^2)
    "drogue_cD": 1,             # Drogue parachute drag coefficent
    "drogue_area": 0.5,         # Drogue parachute area (m^2)
    "main_deploy": 11000        # Main deployment altitude (ft)
    }

# Initialise the state class with initial conditions
State = Structures.initialiseState(initial_conditions)
altitude = [Structures.getAltitude(State)]
time = [State.time]
velocity = [np.linalg.norm(State.vB_E_G)]
acceleration = [np.linalg.norm(Structures.get_aB_I_I(State))]

def shouldContinueLoop():
    if State.time < 700 and State.vB_E_G[0] >= 0:
        return True
    else:
        State.max_altitude = np.round(Structures.getAltitude(State) * 3.28084)
        return State.time < 700


# Main Loop
while shouldContinueLoop():
    # Integrate the DE's in inertial coordinates
    Integrator.eulerIntegration(State)

    altitude.append(Structures.getAltitude(State))
    time.append(State.time)
    velocity.append(State.vB_E_G[0])
    acceleration.append(State.aB_E_G[0])
    iter =+ 1


# Post - Processing
print("Max Altitude: ",State.max_altitude,"ft")
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
