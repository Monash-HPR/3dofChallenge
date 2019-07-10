import numpy as np
from Modules import Transformations
from Modules import Geodesy
from Modules.Forces import Propulsion
from Modules.Forces import Aerodynamics
from Modules.Forces import Inertia

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
        self.reference_area = initial_conditions["reference_area"]
        self.euler_angles = np.array([[0.0], [np.pi/2], [0.0]])
        self.aB_I_I = np.array([[0.0], [0.0], [0.0]])

        # Set inital position

        # Set the geodetic postion from the given coordinates by the user. Geodetic altitude is corrected for
        # an spheroidal Earth and depends on geodetic latitude. NOTE: altitude might be wrong
        geodetic_position = np.array([[0.0], [0.0], [0.0]])
        geodetic_position[0,0] = np.radians(initial_conditions["latitude"])
        geodetic_position[1,0] = np.radians(initial_conditions["longitude"])
        geodetic_position[2,0] = initial_conditions["altitude"]

        # Calculate the geocentric position in cartesian coordinates
        sBI__E = Geodesy.getGeocentricPosition(geodetic_position)

        # Transform this to the Inertial frame (at inital state they coincide as the Earth has not rotated)
        T_IE = Transformations.get_T_EI(self.time)
        self.sBI__I = np.matmul(T_IE,sBI__E)

        # Set initial velocity
        self.vB_E_D = np.array([[0.0], [0.0], [0.0]])                    # Assumes initial velocity is zero w.r.t. Earth
        omegaEI__I = Geodesy.get_omegaEI__I()
        T_DI = Transformations.get_T_DI(self.sBI__I, self.time)
        self.vB_I_I = np.matmul(np.transpose(T_DI),self.vB_E_D) + np.matmul(omegaEI__I,self.sBI__I)

        # Set initial T_BI
        T_GI = Transformations.get_T_GI(self.sBI__I, self.time)
        T_BG = Transformations.get_T_BG(self.euler_angles)
        self.T_BI = np.matmul(T_DI,T_BG)


def initialiseState(initial_conditions):
    return State(initial_conditions)

def getAltitude(State):
    # Returns the altitude
    sBI_norm = np.linalg.norm(State.sBI__I)
    lat = Geodesy.getGeodeticPosition(State.sBI__I,State.time)
    return sBI_norm - np.linalg.norm(Geodesy.getR0(lat[0]))

def get_aB_I_I(State):
    # Function returns the inertial acceleration in inertial coordinates which can be directly integrated using Newton's
    f__B = getForces(State)
    g__G = Inertia.getGravityAcceleration(State)
    T_IB = np.transpose(State.T_BI)
    m = State.mass
    T_IG = np.transpose(Transformations.get_T_GI(State.sBI__I,State.burn_time))
    return 1/m * np.matmul(T_IB,f__B) + np.matmul(T_IG,g__G)

def getForces(State):
    # Returns the force (acceleration) due to propulsion and aerodynamics in body coordinates
    # NOTE: This function requires uprading once wind is implemented as it assumes that velocity and body coordinates
    # the same. Once wind is implemented, the aerodynamic force will be calculate
    T = Propulsion.getThrust(State)
    F = Aerodynamics.getAerodynamicForce(State)
    return  T + F

def get_vB_E_D(State):
    T_DI = Transformations.get_T_DI(State.sBI__I,State.time)
    omegaEI__I = Geodesy.get_omegaEI__I()
    return np.matmul(T_DI,(State.vB_I_I - np.matmul(omegaEI__I,State.sBI__I)))
