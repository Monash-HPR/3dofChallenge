import numpy as np
from Modules import Transformations
from Modules import Geodesy

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
        self.euler_angles = np.array([[0.0], [np.pi/2], [0.0]])
        self.aB_I_I = np.array([[0.0], [0.0], [0.0]])

        # Set inital position

        # Set the geodetic postion from the given coordinates by the user. Geodetic altitude is corrected for
        # an spheroidal Earth and depends on geodetic latitude. NOTE: altitude might be wrong
        geodetic_position = np.array([[0.0], [0.0], [0.0]])
        geodetic_position[0,0] = np.radians(initial_conditions["latitude"])
        geodetic_position[1,0] = np.radians(initial_conditions["longitude"])
        geodetic_position[2,0] = initial_conditions["altitude"] + Geodesy.getR0(geodetic_position[0]) - r_Earth

        # Calculate the geocentric position in cartesian coordinates
        sBI__E = Geodesy.getGeocentricPosition(geodetic_position)

        # Transform this to the Inertial frame (at inital state they coincide as the Earth has not rotated)
        T_IE = Transformations.get_T_EI(self.time)
        self.sBI__I = np.matmul(T_IE,sBI__E)

        # Set initial velocity
        vB_E_D = np.array([[0.0], [0.0], [0.0]])                    # Assumes initial velocity is zero w.r.t. Earth
        omegaEI__I = Transformations.skewSymmetricExpansion(Geodesy.get_WBE__I())
        T_DI = Transformations.get_T_DI(self.sBI__I, self.time)
        self.vB_I_I = np.matmul(np.transpose(T_DI),vB_E_D) + np.matmul(omegaEI__I,self.sBI__I)

        # Set initial T_BI
        T_GI = Transformations.get_T_GI(self.sBI__I, self.time)
        T_BG = Transformations.get_T_BG(self.euler_angles)
        self.T_BI = np.matmul(T_DI,T_BG)


def initialiseState(initial_conditions):
    return State(initial_conditions)

def getAltitude(State):
    # Returns the altitude
    sBI_norm = np.linalg.norm(State.sBI__I)
    return sBI_norm - r_Earth
