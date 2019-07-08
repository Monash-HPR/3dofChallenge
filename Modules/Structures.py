import numpy as np


class State:
    def __init__(self,initial_conditions):
        self.time = initial_conditions["time"]
        self.dt = initial_conditions["dt_initial"]
        self.mass_dry = initial_conditions["mass_dry"]
        self.mass_propellant = initial_conditions["mass_propellant"]
        self.apogee = "false"
        self.sBI__I = np.array([6378137.0, 0.0, 0.0])
        self.vB_I_I = np.array([0.0, 0.0, 0.0])
        self.aB_I_I = np.array([0.0, 0.0, 0.0])

def InitialiseState(initial_conditions):
    return State(initial_conditions)
