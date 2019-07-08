import numpy as np
from Modules import Transformations

# constants
DEG_TO_RAD = np.pi / 180;       # Degrees to radians conversion factor
r_Earth = 6378137.0             # Radius of the Earth (m)


class State:
    def __init__(self,initial_conditions):
        self.time = initial_conditions["time"]
        self.dt = initial_conditions["dt_initial"]
        self.mass_dry = initial_conditions["mass_dry"]
        self.mass_propellant = initial_conditions["mass_propellant"]
        self.mass = self.mass_propellant + self.mass_dry
        self.apogee = "false"
        self.burn_time = initial_conditions["burn_time"]
        self.thrust = initial_conditions["thrust"]

        #set inital position
        self.sB_I_I = np.array([0.0, 0.0, -r_Earth - initial_conditions["altitude"]])
        sBI__G = np.array([[0.0], [0.0], [r_Earth + initial_conditions["altitude"]]])
        print(sBI__G)
        T_DG = initial_T_DG(sBI__G) # Fix this shit
        self.sBI__I = np.matmul(np.matmul(np.transpose(T_DI),T_DG),sBI__G)

        self.vB_I_I = np.array([0.0, 0.0, 0.0])
        self.aB_I_I = np.array([0.0, 0.0, 0.0])

def initialiseState(initial_conditions):
    return State(initial_conditions)

def getAltitude(State):
    # Returns the altitude
    sBI_norm = np.linalg.norm(State.sBI__I)
    return sBI_norm - r_Earth
