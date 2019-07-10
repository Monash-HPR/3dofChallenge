import numpy as np
from Forces import Propulsion
from Forces import Aerodynamics
from Forces import Inertia

def getSpecificForce(State):
    # Returns the specific force (acceleration) due to propulsion and aerodynamics in velocity coordinates
    # NOTE: This function requires uprading once wind is implemented as it assumes that velocity and body coordinates
    # the same. Once wind is implemented, the aerodynamic force will be calculate
    T = Propulsion.getThrust(State)
    F = Aerodynamics.getAerodynamicForce(State)
    m = State.mass
    return  1/m * np.add(T, F)

def get_a_B_I_I(State):
    f_specific__B = getSpecificForce(State)
    
