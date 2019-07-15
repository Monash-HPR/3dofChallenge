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
        self.burn_time = initial_conditions["burn_time"]
        self.thrust = initial_conditions["thrust"]
        self.reference_area = initial_conditions["reference_area"]
        self.euler_angles = np.array([[0.0], [np.pi/2], [0.0]])
        self.lat = initial_conditions["latitude"]
        self.lon = initial_conditions["longitude"]
        self.max_altitude = 0.0;
        self.parachute_cD = initial_conditions["parachute_Cd"]
        self.parachute_area = initial_conditions["parachute_area"]
        self.drogue_cD = initial_conditions["drogue_cD"]
        self.drogue_area = initial_conditions["drogue_area"]
        self.main_deploy = initial_conditions["main_deploy"]


        # Set inital position
        # Calculate the geocentric position in cartesian coordinates
        self.sBE__G = initGeographicPosition(initial_conditions)
        #T_GI = Transformations.get_T_GI(self.lat,self.lon)
        self.sBI__I = self.sBE__G

        # Set initial velocity
        self.vB_E_G = np.array([[0.0], [0.0], [0.0]])          # Assumes initial velocity is zero w.r.t. Earth
        self.vB_I_I = self.vB_E_G

        #Set initial Acceleration
        self.aB_I_I = np.array([[0.0], [0.0], [0.0]])
        self.aB_E_G = np.array([[0.0], [0.0], [0.0]])

def initialiseState(initial_conditions):
    return State(initial_conditions)

def getAltitude(State):
    # Returns the altitude
    sBI_norm = np.linalg.norm(State.sBI__I)
    return sBI_norm - r_Earth

def get_aB_I_I(State):
    # Function returns the inertial acceleration in inertial coordinates which can be directly integrated using Newton's
    f__B = getForces(State)
    g__G = np.array([[Geodesy.GM / (np.linalg.norm(State.sBI__I)**2)], [0.0], [0.0]])
    m = State.mass
    return  1/m * f__B - g__G

def getForces(State):
    # Returns the force (acceleration) due to propulsion and aerodynamics in body coordinates
    # NOTE: This function requires uprading once wind is implemented as it assumes that velocity and body coordinates
    # the same. Once wind is implemented, the aerodynamic force will be calculate
    T = Propulsion.getThrust(State)
    F = Aerodynamics.getAerodynamicForce(State)
    return  T + F

def updateMass(State):
    if State.time < State.burn_time:
        State.mass = State.mass - State.mass_propellant / State.burn_time * State.dt
        return
    return

def initGeographicPosition(initial_conditions):
    lat = np.radians(initial_conditions["latitude"])
    lon = np.radians(initial_conditions["longitude"])
    alt = initial_conditions["altitude"]
    sin_lat = np.sin(lat)
    cos_lat = np.cos(lon)
    sin_lon = np.sin(lon)
    cos_lon = np.cos(lon)
    r = (alt + r_Earth) * cos_lat
    x = r * cos_lon
    y = r * sin_lon
    z = (alt + r_Earth) * sin_lat
    return np.array( [[x], [y], [z]])
