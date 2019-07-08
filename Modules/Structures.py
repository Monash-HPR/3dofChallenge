import numpy as np

# constants
DEG_TO_RAD = np.pi / 180;       # Degrees to radians conversion factor
r_Earth = 6378137.0             # Radius of the Earth (m)


class State:
    def __init__(self,initial_conditions):
        self.time = initial_conditions["time"]
        self.dt = initial_conditions["dt_initial"]
        self.mass_dry = initial_conditions["mass_dry"]
        self.mass_propellant = initial_conditions["mass_propellant"]
        self.apogee = "false"

        #set inital position
        sBI__G = np.array([[DEG_TO_RAD * initial_conditions["latitude"]], [DEG_TO_RAD * initial_conditions["longitude"]], [r_Earth + initial_conditions["altitude"]]])
        print(sBI__G)
        self.sBI__I = np.array([[0.0], [0.0], [0.0]])


        self.vB_I_I = np.array([0.0, 0.0, 0.0])
        self.aB_I_I = np.array([0.0, 0.0, 0.0])

def initialiseState(initial_conditions):
    return State(initial_conditions)
